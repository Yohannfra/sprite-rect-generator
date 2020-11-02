#!/bin/bash

if (( $EUID != 0 )); then
    echo "Please run as root"
    exit 1
fi

set -e

python setup.py install

echo -ne "#!/bin/bash\n\npython3 -m rect_generator \"\$@\"\n" > build/rect_generator
chmod +x build/rect_generator
mkdir -p ~/.local/bin
sudo cp build/rect_generator ~/.local/bin

echo "Done !"
