import sys
import os
import urllib.request
import requests
# TODO try requests
import hashlib
import argparse
import traceback

if len(os.environ) == 0 or 'SCONE_MODE' in os.environ:
    teeMode=True
    outDir="/scone"
else:
    teeMode=False
    outDir="/iexec_out"

download_chunk_size = 1024 * 1024

def md5(fname):
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

if __name__ == "__main__":
    if teeMode:
        print("Starting in enclave")
        sys.stdout.flush()

    print("running with following env:")
    print(os.environ)
    sys.stdout.flush()
    print("Arguments for script: ")
    print(sys.argv)

    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--picture', type=str, 
        default='https://upload.wikimedia.org/wikipedia/commons/thumb/c/cd/Stray_kitten_Rambo002.jpg/1280px-Stray_kitten_Rambo002.jpg',
        help="picture to download")                        
    args = parser.parse_args()
    print(args)
    
    image_path = args.picture
    
    # Simplified URL check
    if image_path.startswith("http"):
        # downloading picture using urllib
        tmp_image_path = os.path.join(outDir,"image.jpg")
        try:
            print("Downloading picture using urllib from ", image_path)
            
            urllib.request.urlretrieve(args.picture, filename=tmp_image_path)
            if not os.path.exists(tmp_image_path):
                print("Failed to download picture")
        except:
            print(traceback.format_exc())

        if os.path.exists(tmp_image_path):
            print("Using image: ", image_path, " md5 hash: ", md5(tmp_image_path))

        tmp_image_path = os.path.join(outDir,"image2.jpg")
        
        try:
            print("Downloading picture using requests from ", image_path)
            r = requests.get(image_path, stream=True)
            with open(tmp_image_path, 'wb') as fd:
                for chunk in r.iter_content(chunk_size=download_chunk_size):
                    fd.write(chunk)

            if not os.path.exists(tmp_image_path):
                print("Failed to download picture")
        except:
            print(traceback.format_exc())
                    
        if os.path.exists(tmp_image_path):
            print("Using image: ", image_path, " md5 hash: ", md5(tmp_image_path))
    else:
        print("Invalid picture URL")
        exit(1)

    


