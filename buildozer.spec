[app]
title = TicTacTower
package.name = tictactower
package.domain = org.marcosbordas

source.dir = .
source.include_exts = py,png,jpg,kv,atlas,ttf,json
source.include_patterns = assets/*.png

version = 0.1.0

requirements = python3==3.12.7,kivy==2.3.1

orientation = portrait
fullscreen = 0

android.archs = arm64-v8a
android.ant = 1
android.api = 35
android.minapi = 24
android.ndk_api = 26
android.accept_sdk_license = True
android.permissions = INTERNET
android.private_storage = False

icon.filename = %(source.dir)s/assets/icon.png
presplash.filename = %(source.dir)s/assets/presplash.png

android.keystore = keys/tictactower.keystore
android.storepass = tictactower2026
android.keyalias = tictactower
android.keypass = tictactower2026

[buildozer]
log_level = 2
warn_on_root = 1