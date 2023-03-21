using Gumbo: parsehtml, tag, getattr
using HTTP
using AbstractTrees: PreOrderDFS
using URIs: splitpath

"""
    download_pics(url)

Download all images from a given url.

E.g `download_pic("https://www.foxwq.com/news/listid/id/13882.html")`
"""
function download_pics(url)
    r = HTTP.get(url)

    r_parsed = parsehtml(String(r.body))

    img_urls = []
    for elem in PreOrderDFS(r_parsed.root[2])
        try
            if tag(elem) == :img
                a = getattr(elem, "src")
                println(a)
                push!(img_urls, a)
            end
        catch
            # Nothing needed here
        end
    end

    files_to_download = filter(x -> x[1:5] == "https", img_urls)

    out_file_names = map(x -> x[end], splitpath.(files_to_download))


    dl_paths = joinpath.(Ref("./assets/"), out_file_names)

    download.(files_to_download, dl_paths)

    out_file_names
end

