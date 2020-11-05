#!/bin/bash

if (( $EUID != 0 )); then
    echo "Please run as root"
    exit 1
fi


set -e

USER_CALLING=`logname`
USER_HOME=`eval echo "~$USER_CALLING"`
TARGET_DIRECTORY="$USER_HOME/.local/bin"

python3 setup.py install

echo -ne "#!/bin/bash\n\npython3 -m rect_generator \"\$@\"\n" > build/rect_generator
chmod +x build/rect_generator
mkdir -p $TARGET_DIRECTORY
cp build/rect_generator $TARGET_DIRECTORY

echo "Done !"
echo "The binary is in $TARGET_DIRECTORY"
