using Gumbo: parsehtml, tag, getattr
using HTTP
using AbstractTrees: PreOrderDFS

r = HTTP.get("https://www.foxwq.com/news/listid/id/13882.html")

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

using URIs: splitpath

dl_paths = joinpath.(Ref("./assets/"), map(x -> x[end], splitpath.(files_to_download)))

download.(files_to_download, dl_paths)

