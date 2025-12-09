#!/usr/bin/env bash
set -euo pipefail

# This script creates a disk image, formats it as ext4, and mounts it to /srv/uploads
IMG_PATH=/var/lib/uploads.img
IMG_SIZE=50G

# create parent dir and image file (sparse)
sudo mkdir -p "$(dirname "$IMG_PATH")"
sudo truncate -s $IMG_SIZE "$IMG_PATH"

# find and attach a free loop device; prints the device path (e.g., /dev/loop0)
LOOP_DEV=$(sudo losetup --find --show "$IMG_PATH")
echo "loop device: $LOOP_DEV"

# make ext4 filesystem and label it (label optional)
sudo mkfs.ext4 -F -L uploads_img "$LOOP_DEV"

# get UUID of the new filesystem
UUID=$(sudo blkid -s UUID -o value "$LOOP_DEV")
echo "UUID=$UUID"

# mount it to /srv/uploads
MOUNT_POINT=/srv/uploads
sudo mkdir -p "$MOUNT_POINT"
sudo mount "$LOOP_DEV" "$MOUNT_POINT"

# set ownership and permissions
APP_USER=appuser
APP_GROUP=www-data

# Create app user/group if missing (safe to run even if exists)
if ! id -u "$APP_USER" >/dev/null 2>&1; then
  sudo useradd --system --no-create-home --group "$APP_GROUP" "$APP_USER" || true
fi

# create system app user/group if they do not exist (optional)
# sudo useradd --system --no-create-home --group "$APP_GROUP" "$APP_USER" || true
sudo chown -R ${APP_USER}:${APP_GROUP} "$MOUNT_POINT"
sudo chmod -R 750 "$MOUNT_POINT"

# Recommended fstab entry (replace UUID value printed earlier)
echo "UUID=$UUID  /srv/uploads  ext4  defaults,noatime  0  2" | sudo tee -a /etc/fstab

sudo umount "$MOUNT_POINT"
sudo mount -a
mount | grep "$MOUNT_POINT"
echo "Disk image created, formatted, and mounted at $MOUNT_POINT"
