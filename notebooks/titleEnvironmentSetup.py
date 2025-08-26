# #@title Environment Setup

from pathlib import Path

OPTIONS = {}

USE_GOOGLE_DRIVE = True  #@param {type:"boolean"}
UPDATE_COMFY_UI = True  #@param {type:"boolean"}
USE_COMFYUI_MANAGER = True  #@param {type:"boolean"}
INSTALL_CUSTOM_NODES_DEPENDENCIES = True  #@param {type:"boolean"}
OPTIONS['USE_GOOGLE_DRIVE'] = USE_GOOGLE_DRIVE
OPTIONS['UPDATE_COMFY_UI'] = UPDATE_COMFY_UI
OPTIONS['USE_COMFYUI_MANAGER'] = USE_COMFYUI_MANAGER
OPTIONS['INSTALL_CUSTOM_NODES_DEPENDENCIES'] = INSTALL_CUSTOM_NODES_DEPENDENCIES

current_dir = !pwd
WORKSPACE = f"{current_dir[0]}/ComfyUI"

if OPTIONS['USE_GOOGLE_DRIVE']:
    !echo "Mounting Google Drive..."
    %cd /

    from google.colab import drive
    drive.mount('/content/drive')

    WORKSPACE = "/content/drive/MyDrive/ComfyUI"
    %cd /content/drive/MyDrive

![ ! -d $WORKSPACE ] && echo -= Initial setup ComfyUI =- && git clone https://github.com/comfyanonymous/ComfyUI
%cd $WORKSPACE

if OPTIONS['UPDATE_COMFY_UI']:
  !echo -= Updating ComfyUI =-

  # Correction of the issue of permissions being deleted on Google Drive.
  ![ -f ".ci/nightly/update_windows/update_comfyui_and_python_dependencies.bat" ] && chmod 755 .ci/nightly/update_windows/update_comfyui_and_python_dependencies.bat
  ![ -f ".ci/nightly/windows_base_files/run_nvidia_gpu.bat" ] && chmod 755 .ci/nightly/windows_base_files/run_nvidia_gpu.bat
  ![ -f ".ci/update_windows/update_comfyui_and_python_dependencies.bat" ] && chmod 755 .ci/update_windows/update_comfyui_and_python_dependencies.bat
  ![ -f ".ci/update_windows_cu118/update_comfyui_and_python_dependencies.bat" ] && chmod 755 .ci/update_windows_cu118/update_comfyui_and_python_dependencies.bat
  ![ -f ".ci/update_windows/update.py" ] && chmod 755 .ci/update_windows/update.py
  ![ -f ".ci/update_windows/update_comfyui.bat" ] && chmod 755 .ci/update_windows/update_comfyui.bat
  ![ -f ".ci/update_windows/README_VERY_IMPORTANT.txt" ] && chmod 755 .ci/update_windows/README_VERY_IMPORTANT.txt
  ![ -f ".ci/update_windows/run_cpu.bat" ] && chmod 755 .ci/update_windows/run_cpu.bat
  ![ -f ".ci/update_windows/run_nvidia_gpu.bat" ] && chmod 755 .ci/update_windows/run_nvidia_gpu.bat

  !git pull

!echo -= Install dependencies =-
!pip3 install accelerate
!pip3 install einops transformers>=4.28.1 safetensors>=0.4.2 aiohttp pyyaml Pillow scipy tqdm psutil tokenizers>=0.13.3
!pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
!pip3 install torchsde
!pip3 install kornia>=0.7.1 spandrel soundfile sentencepiece
!pip3 install uv
!pip3 install av
!pip3 install alembic
!pip install comfyui-embedded-docs --no-deps
!pip install mkdocs-material
!pip install mkdocs-mermaid2-plugin

if OPTIONS['USE_COMFYUI_MANAGER']:
  %cd custom_nodes

  # Correction of the issue of permissions being deleted on Google Drive.
  ![ -f "ComfyUI-Manager/check.sh" ] && chmod 755 ComfyUI-Manager/check.sh
  ![ -f "ComfyUI-Manager/scan.sh" ] && chmod 755 ComfyUI-Manager/scan.sh
  ![ -f "ComfyUI-Manager/node_db/dev/scan.sh" ] && chmod 755 ComfyUI-Manager/node_db/dev/scan.sh
  ![ -f "ComfyUI-Manager/node_db/tutorial/scan.sh" ] && chmod 755 ComfyUI-Manager/node_db/tutorial/scan.sh
  ![ -f "ComfyUI-Manager/scripts/install-comfyui-venv-linux.sh" ] && chmod 755 ComfyUI-Manager/scripts/install-comfyui-venv-linux.sh
  ![ -f "ComfyUI-Manager/scripts/install-comfyui-venv-win.bat" ] && chmod 755 ComfyUI-Manager/scripts/install-comfyui-venv-win.bat

  ![ ! -d ComfyUI-Manager ] && echo -= Initial setup ComfyUI-Manager =- && git clone https://github.com/ltdrdata/ComfyUI-Manager
  %cd ComfyUI-Manager
  !git pull

%cd $WORKSPACE

if OPTIONS['INSTALL_CUSTOM_NODES_DEPENDENCIES']:
  !echo -= Install custom nodes dependencies =-
  !pip install GitPython
  !python custom_nodes/ComfyUI-Manager/cm-cli.py restore-dependencies
