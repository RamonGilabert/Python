# All the prints that will appear in the app will be mainly logs, don't really
# want to put everywhere a '# logs', so this is a general rule accross the
# app.

# The app description will appear in the general README and the particular
# README in the folder this file is contained in.

from app.app import App

if __name__ == '__main__':
    app = App()
