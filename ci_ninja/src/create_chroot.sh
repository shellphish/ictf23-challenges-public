#!/bin/bash

# Set chroot directory
CHROOT_DIR="./chroot"

# Ensure directory structure
mkdir -p $CHROOT_DIR/bin
mkdir -p $CHROOT_DIR/{lib,lib64}

add_to_chroot() {
    BIN_FILE=$(which $1)

    # Copy binary to chroot directory
    cp $BIN_FILE $CHROOT_DIR/bin/

    # Copy dependencies
    for i in $(ldd $BIN_FILE | awk '{print $3}' | grep "^/") $(ldd $BIN_FILE | awk '{print $1}' | grep "^/")
    do
       cp --parents $i $CHROOT_DIR
    done
}

add_to_chroot cat