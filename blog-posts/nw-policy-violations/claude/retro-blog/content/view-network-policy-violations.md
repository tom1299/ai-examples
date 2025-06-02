+++
title = "Detecting Network Policy Violations with Cilium: Moving from Calico"
date = 2024-12-06T10:00:00Z
draft = false
<!-- Not aligned with any of the tags I had before-->
tags = ["cilium", "kubernetes", "network-policy", "observability", "calico", "troubleshooting"]
<!-- Not aligned with any of the categories I had before-->
categories = ["networking", "kubernetes"]
+++

## Problem: Limited Network Policy Observability with Calico

Currently using Calico in our Kubernetes cluster, we found it challenging to detect network policy violations effectively. Calico doesn't provide comprehensive observability for policy violations out of the box, making troubleshooting network connectivity issues difficult and time-consuming.

## Solution: Leveraging Cilium's Enhanced Observability

After researching alternatives, we decided to migrate to [Cilium](https://cilium.io/) which promises better 
<!-- Why use "we" all the time? -->
observability capabilities by default. As newcomers to Cilium, our goal was to get network policy violation detection working quickly and efficiently.

### Deployment Configuration

We deployed Cilium using Helm with specific parameters to enable enhanced observability and policy violation tracking:

```bash
helm install cilium cilium/cilium \
    --set debug.verbose="flow policy kvstore envoy datapath" \
    --set hubble.dropEventEmitter.enabled=true \
    --set hubble.dropEventEmitter.interval=5s
```

These parameters enable:
- **debug.verbose**: Detailed logging for flow, policy, kvstore, envoy, and datapath components
- **hubble.dropEventEmitter.enabled**: Enables emission of packet drop events
- **hubble.dropEventEmitter.interval**: Sets the interval for drop event emission to 5 seconds

### Testing and Verification

To test the network policy violation detection, we deployed test manifests in the `cni-test` namespace with nginx pods and network policies that would deny certain traffic.

#### Step 1: Get Target Pod IP
```bash
$ kubectl get pods -n cni-test -l app=nginx -o jsonpath='{.items[*].status.podIP}'
10.0.0.226
```

#### Step 2: Run Network Troubleshooting Pod
```bash
$ kubectl run -ti netshot --image=nicolaka/netshoot -n cni-test
```

#### Step 3: Attempt Blocked Connection
```bash
$ curl 10.0.0.226:80
# Connection will be blocked by network policy
```

#### Step 4: Monitor Kubernetes Events
```bash
$ kubectl get events -n cni-test --watch
0s    Warning   PacketDrop    pod/netshot    Outgoing packet dropped (policy_denied) to cni-test/nginx-5c754d96b-6r7x2 (10.0.0.226) TCP/80
```

**Success!** Policy violations are now clearly visible in Kubernetes events, showing exactly which packets were dropped and why.

#### Step 5: Advanced Monitoring with Hubble
For more detailed analysis, we can also use Hubble's CLI tool:

```bash
$ kubectl exec -ti -n kube-system cilium-7z4ct -c cilium-agent -- hubble observe -f --from-label run=netshot
May 31 05:24:48.077: cni-test/netshot:47302 (ID:59296) <> cni-test/nginx-5c754d96b-6r7x2:80 (ID:2290) policy-verdict:none EGRESS DENIED (TCP Flags: SYN)
May 31 05:24:48.077: cni-test/netshot:47302 (ID:59296) <> cni-test/nginx-5c754d96b-6r7x2:80 (ID:2290) Policy denied DROPPED (TCP Flags: SYN)
```

**Note:** Hubble CLI access requires exec privileges to pods in the `kube-system` namespace, which might not be available in managed Kubernetes clusters.

## Results

The migration to Cilium successfully solved our network policy observability challenges:

1. **Immediate Visibility**: Policy violations are now visible directly in Kubernetes events
2. **Detailed Information**: Events show source, destination, protocol, and reason for blocking
3. **Real-time Monitoring**: Drop events are emitted every 5 seconds for continuous monitoring
4. **Enhanced Debugging**: Hubble provides additional detailed flow information for deeper analysis

## Conclusion

Cilium's built-in observability features significantly improve network policy troubleshooting compared to Calico. The ability to see policy violations in Kubernetes events makes it much easier to identify and resolve connectivity issues. Our next step is to investigate which specific policies and rules are being violated to further optimize our network security configuration.

<!-- Marketing blablabla -->
For teams struggling with network policy visibility, Cilium provides an excellent solution with minimal configuration overhead. The [Cilium documentation](https://docs.cilium.io/en/stable/installation/k8s-install-helm/) offers comprehensive guidance for getting started with enhanced observability features.

<!-- No links to existing content -->
<!-- Style is not mine -->