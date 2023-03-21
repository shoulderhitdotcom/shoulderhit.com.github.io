import face_recognition as fr

def get_faces(path):
    image = fr.load_image_file(path)
    face_locations = fr.face_locations(image)
    # print(face_locations)
    # print(fr.face_encodings(image, face_locations)[0])
    return face_locations


def get_faces_from_list(list):
    return [get_faces(path) for path in list]

# print(get_faces("./assets/t_16725020750.png"))
# print(get_faces("./assets/t_16725020751.png"))
# print(get_faces("./assets/t_16725020752.png"))
# print(get_faces("./assets/t_16725020753.png"))
# print(get_faces("./assets/t_16725020754.png"))
# print(get_faces("./assets/t_16725020755.png"))