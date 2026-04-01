# Using python to install libraries and frameworks
python3.14 -m pip install -r server/requirements.txt

# Create .blueclawai to the user path
mkdir ~/.blueclawai

# Copying files to the .blueclawai
cp blueclawai ~/.blueclawai/blueclawai
cp app.py ~/.blueclawai/app.py

# Add PATH to .blueclawai
echo 'export PATH=$PATH":$HOME/.blueclawai"' >> ~/.zprofile
echo 'export PATH=$PATH":$HOME/.blueclawai"' >> ~/.bash_profile

# Reload the profile files
source ~/.zprofile    
source ~/.bash_profile
