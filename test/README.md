# MiniCluster

We are going to use the [Flux Operator](https://github.com/flux-framework/flux-operator) to create a MiniCluster. This means you'll have MPIs with Flux Framework. Install the flux operator:

```bash
kubectl apply -f ./flux-operator.yaml
```

Create the MiniCluster

```bash
kubectl apply -f ./minicluster.yaml
```

Shell into the lead broker pod:

```bash
kubectl exec -it flux-sample-0-xxxx bash
```

Connect to the broker socket:

```bash
flux proxy local:///mnt/flux/view/run/flux/local bash
```

See resources!

```bash
flux resource list
```

Set environment variables and run the OSU benchmarks. We tested for each of hpc-x (most performant) and OpenMPI (slower).

```bash
# hpc-x environment variables
export LD_LIBRARY_PATH=/opt/hpcx-v2.19-gcc-mlnx_ofed-ubuntu22.04-cuda12-x86_64/hpcx-rebuild/lib:/opt/hpcx-v2.19-gcc-mlnx_ofed-ubuntu22.04-cuda12-x86_64/hcoll/lib
export PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/opt/hpcx-v2.19-gcc-mlnx_ofed-ubuntu22.04-cuda12-x86_64/hpcx-rebuild/bin

# hpc-x flux submit
flux run --env LD_LIBRARY_PATH=$LD_LIBRARY_PATH --env OMPI_MCA_btl_openib_warn_no_device_params_found=0 --env PATH=$PATH --env UCX_TLS=ib,sm,self --env UCX_NET_DEVICES=mlx5_0:1 -N2 -n2 /opt/hpcx-v2.19-gcc-mlnx_ofed-ubuntu22.04-cuda12-x86_64/hpcx-rebuild/tests/osu-micro-benchmarks/osu_latency
```

The output, really speedy:

```console
 OSU MPI Latency Test v7.2
# Size          Latency (us)
# Datatype: MPI_CHAR.
1                       1.61
2                       1.60
4                       1.61
8                       1.61
16                      1.61
32                      1.75
64                      1.80
128                     1.84
256                     2.35
512                     2.44
1024                    2.60
2048                    2.77
4096                    3.56
8192                    4.07
16384                   5.33
32768                   7.00
65536                   9.07
131072                 13.73
262144                 17.32
524288                 28.01
1048576                49.60
2097152                92.92
4194304               177.15
```

Note that there is a warning but it doesn't seem to impact it being fast. Now OpenMPI. Note that performance was the same with the same osu build above as the build with this MPI instead.

```bash
# openmpi
export LD_LIBRARY_PATH=/opt/openmpi-5.0.5/lib:/opt/hpcx-v2.19-gcc-mlnx_ofed-ubuntu22.04-cuda12-x86_64/hcoll/lib
export PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/opt/openmpi-5.0.5/bin:$PATH

flux run --env LD_LIBRARY_PATH=$LD_LIBRARY_PATH -opmi=pmix --env PATH=$PATH --env UCX_TLS=ib,self --env UCX_NET_DEVICES=mlx5_0:1 -N2 -n2 /opt/hpcx-v2.19-gcc-mlnx_ofed-ubuntu22.04-cuda12-x86_64/hpcx-rebuild/tests/osu-micro-benchmarks/osu_latency
```
```console
# OSU MPI Latency Test v7.2
# Size          Latency (us)
# Datatype: MPI_CHAR.
1                       2.46
2                       3.31
4                       3.31
8                       3.71
16                      4.77
32                      5.96
64                      4.96
128                     6.06
256                     4.90
512                     4.98
1024                    5.99
2048                    5.30
4096                   19.22
8192                   16.43
16384                  15.83
32768                  17.30
65536                  15.56
131072                 37.31
262144                 51.75
524288                110.92
1048576               259.63
2097152               363.13
4194304               522.29
```
