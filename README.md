# AKS Infiniband Installer

We are trying to get Infiniband working on AKS, and this small series of steps will help.
We are using the build here to install the drivers to the nodes, and then the [Mellanox/k8s-rdma-shared-dev-plugin](https://github.com/Mellanox/k8s-rdma-shared-dev-plugin/tree/master/deployment/k8s) to provide a CNI to enable Infiniband on the pods.

## 1. Build Image

You'll need to have the driver that matches your node version. Nvidia has disabled allowing wget / curl of the file so you'll need to agree to their license agreement and download it [from this page](https://network.nvidia.com/products/infiniband-drivers/linux/mlnx_ofed/). Note that we follow the instructions [here](https://docs.nvidia.com/networking/display/mlnxofedv461000/installing+mellanox+ofed) to install it with the daemonset. Then update in the Dockerfile:

1. The base image to use (e.g., ubuntu:22.04) to match your driver
2. The `COPY` directive to copy the ISO into the directory
3. The [driver-installation.yaml](driver-installation.yaml) that references it

## 2. Cluster Setup

When you create your cluster, you need to do the following.

```bash
# Enable Infiniband for your AKS cluster 
az feature register --name AKSInfinibandSupport --namespace Microsoft.ContainerService

# Check the status
az feature list -o table --query "[?contains(name, 'Microsoft.ContainerService/AKSInfinibandSupport')].{Name:name,State:properties.state}"

# Register when ready
az provider register --namespace Microsoft.ContainerService
```

Some additional notes - you need an AKS nodepool with RDMA-capable skus (see [here])

## 3. Node Init

Note that if you shell into a node (install `kubectl node-shell`) if you install `ibverbs-utils` and do `ibv_devices` it will be empty. Let's try to install infiniband next, and we will use a container that is also built with ubuntu 22.04 drivers. I was originally looking at [https://github.com/Mellanox/ib-kubernetes](https://github.com/Mellanox/ib-kubernetes). You can just do but then I switched to the approach we have here. Let's first install the drivers:

```bash
kubectl apply -f ./driver-installation.yaml
```

When they are done, here is how to check that it was successful - this isn't perfect but it works. Basically we want to see that the ib0 device is up.

```bash
for pod in $(kubectl get pods -o json | jq -r .items[].metadata.name)
do
   kubectl exec -it $pod -- nsenter -t 1 -m /usr/sbin/ip link | grep 'ib0:'
done
```

That should equal the number of nodes. Then.

```bash
kubectl delete -f ./driver-installation.yaml
```

If you want to test Infiniband, you need to use ping.

```bash
# First node
kubectl node-shell aks-userpool-14173555-vmss000000
ibv_rc_pingpong

# Second node
kubectl node-shell aks-userpool-14173555-vmss000001 
ibv_rc_pingpong aks-userpool-14173555-vmss000000
```

Apply the daemonset to make it available to pods:

```bash
kubectl apply -k ./daemonset/
```

Note that the [ucx perftest](https://github.com/openucx/ucx/tree/master?tab=readme-ov-file#ucx-performance-test) I have found useful.
We will add examples with HPC applications (or a link to a repository with them) soon.

## License

HPCIC DevTools is distributed under the terms of the MIT license.
All new contributions must be made under this license.

See [LICENSE](https://github.com/converged-computing/cloud-select/blob/main/LICENSE),
[COPYRIGHT](https://github.com/converged-computing/cloud-select/blob/main/COPYRIGHT), and
[NOTICE](https://github.com/converged-computing/cloud-select/blob/main/NOTICE) for details.

SPDX-License-Identifier: (MIT)

LLNL-CODE- 842614

