# ml-toolbox
Useful docker images with cuda, Jupyter and ml/dl libraries(pytorch, tf, jax, trax, haiku)

## Usage:
```bash
docker run -d 
  --name toolbox 
  --gpus=all --ipc=host 
  -v /some-large-storage:/workspace/data 
  -v /some-fast-storage:/workspace/notebooks 
  -p 8888:8888 -p 6006:6006 
rexhaif/ml-toolbox:latest
```
- some-fast-storage stands for a directory in mount path of your ssd's, if you have one
- some-large-storage stands for a directory in a mount path of your hdd/raid/nfs

I encourage you to use this two directories approach, where you store your large datasets in /workspace/data and store your notebooks/code/small data in /workspace/notebooks. However, you can easily mount both paths into the same device or don't mount them at all.

After executing following command you will be able to access your jupyter notebook at http://your-hostname-or-ip:8888/lab, default password is ``` change-me-asap ```. You are encouraged to change it, i'll provide necessary scripts later.
