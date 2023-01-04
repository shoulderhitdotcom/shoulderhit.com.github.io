include("download-pics.jl")

using YAML

using PyCall

# fr = pyimport("face_recognition")
py"""
import sys
sys.path.insert(0, "./")
"""

fr = pyimport("facereg")


"""
    process(filepath)

Processes the md file by first extracting the source and then processing each image
"""


function extract_front_matter(filepath)
    yaml_str = ""
    not_found_end_of_front_matter = false

    open(filepath) do file
        if readline(file) == "---"
            oneline = readline(file)
            while oneline != "---"
                yaml_str = yaml_str * "\n" * oneline
                if eof(file)
                    not_found_end_of_front_matter = true
                    break
                end
                oneline = readline(file)
            end
        end
    end

    if not_found_end_of_front_matter
        @warn "Front matter YAML not found; no processing done"
        return
    end

    ## assume front matter found
    front_matter = YAML.load(yaml_str)
    front_matter
end

function process(filepath)
    # extract the YAML front matter
    front_matter = extract_front_matter(filepath)
    if haskey(front_matter, "source")
        dl_pics_path = download_pics(front_matter["source"])
        dl_pics_path = joinpath.(Ref("./assets/"), dl_pics_path)
        return fr.get_faces_from_list(dl_pics_path)
    end

end




