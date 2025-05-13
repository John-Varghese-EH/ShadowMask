#!/bin/bash

# Create DMG
create-dmg \
  --volname "ShadowMask" \
  --volicon "src/shadowmask/assets/icon.icns" \
  --window-pos 200 120 \
  --window-size 800 400 \
  --icon-size 100 \
  --icon "ShadowMask.app" 200 190 \
  --hide-extension "ShadowMask.app" \
  --app-drop-link 600 185 \
  "dist/ShadowMask.dmg" \
  "dist/ShadowMask.app" 
