import os.path
import shutil

from generator import generate_page

separator = "==========================="

def main():
    print("static site generator")
    print("Starting...")
    print(separator)

    base_dir = os.path.dirname(os.path.dirname(__file__))
    static_dir = os.path.join(base_dir, "static")
    public_dir = os.path.join(base_dir, "public")

    print(f"Base dir: {base_dir}")
    print(f"Static dir: {static_dir}")
    print(f"Public dir: {public_dir}")

    print(separator)

    print("Does the public folder exist?")
    if os.path.exists(public_dir):
        print("public folder already exists. Removing it now")
        shutil.rmtree(public_dir)
    else:
        print("no public folder found")

    print("Does the static folder exist?")
    if os.path.exists(static_dir):
        print("Yes")
    else:
        print("No. aborting...")
        exit(1)

    print(separator)

    print("Creating brand new public folder")
    os.mkdir(public_dir)

    copy_dir(static_dir, public_dir)

    print(separator)

    generate_page(
        os.path.join(base_dir, 'content', 'index.md'),
        os.path.join(base_dir, 'template.html'),
        os.path.join(public_dir, 'index.html')
    )


def copy_dir(src_path, dest_path):
    print(f"copying contents from {src_path} to {dest_path}")
    objects = os.listdir(src_path)

    for item in objects:
        object_src_path = os.path.join(src_path, item)
        object_dest_path = os.path.join(dest_path, item)

        if os.path.isdir(object_src_path):
            print("copy_dir: creating dir: " + object_dest_path)
            os.mkdir(object_dest_path)
            copy_dir(object_src_path, object_dest_path)
        if os.path.isfile(object_src_path):
            print(f"copying file: {object_src_path}")
            shutil.copy(object_src_path, object_dest_path)



if __name__ == '__main__':
    main()