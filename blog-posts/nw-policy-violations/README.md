## Context: Blog entry
## Constraints
* Allign any generated content with regards to style and structure with the already existing content
* Create links to already existing content where possible
* If possible try to relate the new content to already existing content and add links
* Fetch any webpage necessary. For example: https://github.com/cilium/cilium/tree/v1.17.4/install/kubernetes/cilium

## Task
Add a blog post in the file retro-blog/content/view-network-policy-violations.md for the task that I did which is described in brief here:
### Problem:
* Currently using calico in current project
* Finding it hard to detect network policy violations (not supported by calico out of the box)
### Idea
* Use cilium which promises better observabiltiy per default
* Currently newbie to cilium, aim to get thngs working fast
### Solution:
* Deploy with helm using specific parameters:
    --set debug.verbose="flow policy kvstore envoy datapath" \
    --set hubble.dropEventEmitter.enabled=true \
    --set hubble.dropEventEmitter.interval=5s
### Test
* Deployed manifests in cni-test (briefly describe)
* Get the ip of one of the nginx pods: kubectl get pods -n cni-test -l app=nginx -o jsonpath='{.items[*].status.podIP}'
* Run network troubleshooting Pod and try to access using curl:
kubectl run -ti netshot --image=nicolaka/netshoot -n cni-test
curl <pod-id> 80
* Look at the events:
kubectl get events -n cni-test --watch
0s          Warning   PacketDrop          pod/netshot                  Outgoing packet dropped (policy_denied) to cni-test/nginx-5c754d96b-6r7x2 (10.0.0.226) TCP/80
Success: Policy violations can be discovered by just looking at the events
* Violations can also be viewd using "hubble":
$ kubectl exec -ti -n kube-system cilium-7z4ct -c cilium-agent -- hubble observe -f --from-label run=netshot
May 31 05:24:48.077: cni-test/netshot:47302 (ID:59296) <> cni-test/nginx-5c754d96b-6r7x2:80 (ID:2290) policy-verdict:none EGRESS DENIED (TCP Flags: SYN)
May 31 05:24:48.077: cni-test/netshot:47302 (ID:59296) <> cni-test/nginx-5c754d96b-6r7x2:80 (ID:2290) Policy denied DROPPED (TCP Flags: SYN)
Notet that for this the user must have priviliges to do an "exec" in the Pods in the namespace "kube-system" which might not be the case for managed clusters

### Conclustion
* Write 2 to 3 sentences
* Where to go from here: Next step is to trying to get more information about why the packages have been dropped. For example which policy / rules where violated

Idea:
* Help generate blog post based on commands and short description
* Not whole content but good base for continuing editing
* Goal: Save time writting these posts

First try:
* VSCdoe CoPilot
* Agent mode Claude Sonnet 4
* Prompt: See above
* Workspace / Codebase: blog project and ci-cd project. Additional context supplied: Folder retro-blog, folder for kind cluster
* Unfortunately hang => Screenshot from protocoll Screenshot from 2025-05-31 07-56-04.png
* Logs:
2025-05-31 07:37:36.564 [error] CodeWindow: detected unresponsive
2025-05-31 07:37:51.565 [error] CodeWindow unresponsive samples:
<1>
    at iLe.a (vscode-file://vscode-app/usr/share/code/resources/app/out/vs/workbench/workbench.desktop.main.js:66:127746)
    at iLe.a (vscode-file://vscode-app/usr/share/code/resources/app/out/vs/workbench/workbench.desktop.main.js:66:127844)
    at iLe.apply (vscode-file://vscode-app/usr/share/code/resources/app/out/vs/workbench/workbench.desktop.main.js:66:127666)
    at vscode-file://vscode-app/usr/share/code/resources/app/out/vs/workbench/workbench.desktop.main.js:66:128197
    at Array.forEach (<anonymous>)
    at ZOi (vscode-file://vscode-app/usr/share/code/resources/app/out/vs/workbench/workbench.desktop.main.js:66:128184)
    at hEt (vscode-file://vscode-app/usr/share/code/resources/app/out/vs/workbench/workbench.desktop.main.js:66:135982)
    at foe.updateOptions (vscode-file://vscode-app/usr/share/code/resources/app/out/vs/workbench/workbench.desktop.main.js:66:134109)
    at Ca.updateOptions (vscode-file://vscode-app/usr/share/code/resources/app/out/vs/workbench/workbench.desktop.main.js:274:12435)
    at hge.z (vscode-file://vscode-app/usr/share/code/resources/app/out/vs/workbench/workbench.desktop.main.js:837:27940)
* From prompt I can see that the context was not set right.

Second try:
* Same prompt
* Context files and folders:
Complete kind-local-6, specifically the install.sh
Changes to prompt:
The emphasis of the post should be what I did in order to enable the visibility of policy violations during helm install and how I then was able to view them.
New prompt:

## Context: Blog entry
## Constraints
* Allign any generated content with regards to style and structure with the already existing content
* Create links to already existing content where possible
* If possible try to relate the new content to already existing content and add links
* Fetch any webpage necessary. For example: https://github.com/cilium/cilium/tree/v1.17.4/install/kubernetes/cilium

## Task
Add a blog post in the file retro-blog/content/view-network-policy-violations.md.
The emphasis of the post should be what I did in order to enable the visibility of policy violations during helm install and how I then was able to view them.
The task that I did which are described in brief here:
### Problem:
* Currently using calico in current project
* Finding it hard to detect network policy violations (not supported by calico out of the box)
### Idea
* Use cilium which promises better observabiltiy per default
* Currently newbie to cilium, aim to get thngs working fast
### Solution:
* Deploy with helm using specific parameters:
    --set debug.verbose="flow policy kvstore envoy datapath" \
    --set hubble.dropEventEmitter.enabled=true \
    --set hubble.dropEventEmitter.interval=5s
### Test
* Deployed manifests in cni-test (briefly describe)
* Get the ip of one of the nginx pods: kubectl get pods -n cni-test -l app=nginx -o jsonpath='{.items[*].status.podIP}'
* Run network troubleshooting Pod and try to access using curl:
kubectl run -ti netshot --image=nicolaka/netshoot -n cni-test
curl <pod-id> 80
* Look at the events:
kubectl get events -n cni-test --watch
0s          Warning   PacketDrop          pod/netshot                  Outgoing packet dropped (policy_denied) to cni-test/nginx-5c754d96b-6r7x2 (10.0.0.226) TCP/80
Success: Policy violations can be discovered by just looking at the events
* Violations can also be viewd using "hubble":
$ kubectl exec -ti -n kube-system cilium-7z4ct -c cilium-agent -- hubble observe -f --from-label run=netshot
May 31 05:24:48.077: cni-test/netshot:47302 (ID:59296) <> cni-test/nginx-5c754d96b-6r7x2:80 (ID:2290) policy-verdict:none EGRESS DENIED (TCP Flags: SYN)
May 31 05:24:48.077: cni-test/netshot:47302 (ID:59296) <> cni-test/nginx-5c754d96b-6r7x2:80 (ID:2290) Policy denied DROPPED (TCP Flags: SYN)
Notet that for this the user must have priviliges to do an "exec" in the Pods in the namespace "kube-system" which might not be the case for managed clusters

### Conclustion
* Write 2 to 3 sentences
* Where to go from here: Next step is to trying to get more information about why the packages have been dropped. For example which policy / rules where violated

### Output second try
* Something was generated but:
	* Did not follow prompt in details
	* Was not alligned with other blog posts
* Verdict:
	* Not really usuable
* Improvments:
	* Try to provide better context
	* Use custom instructions
	* Give better examples
	* Use some other tool => Create a static setup for context


## Use claude
1. Setup msc server: https://github.com/github/github-mcp-server
2. Use the retro-blog project as context: https://github.com/github/github-mcp-server#resources
   Note that this gives access to all files in all repositories. Use https://github.com/github/github-mcp-server#resources prompts to limit the context to the retro-blog project.

3. Setup with mcp configuration here: /home/reuhl/git/github/ai-examples/blog-posts/nw-policy-violations/claude/mcp.json

4. Prompt:
`Create the blog post as described in BLOG_POST.md`

5. Protocol:
```
● I'll read the BLOG_POST.md file to understand what blog post needs to be created.

● Read(BLOG_POST.md)…
  ⎿  Read 40 lines (ctrl+r to expand)

● Now I need to check the existing blog content structure to align with the style. Let me check if there's a way to access the retro-blog repository.

● Update Todos
  ⎿  ☐ Examine existing blog post structure and style from retro-blog repository
     ☐ Create the blog post file with proper structure and content
     ☐ Fetch Cilium installation documentation from GitHub
     ☐ Add relevant links to existing content where possible

● Update Todos
  ⎿  ☐ Examine existing blog post structure and style from retro-blog repository
     ☐ Create the blog post file with proper structure and content
     ☐ Fetch Cilium installation documentation from GitHub
     ☐ Add relevant links to existing content where possible

● Let me search for information about the retro-blog repository structure. Since I need to align with existing content style, I'll search for the repository.

● Task(Search for retro-blog repository)…
  ⎿  Done (9 tool uses · 26.6k tokens · 3m 10.5s)

● Update Todos
  ⎿  ☒ Examine existing blog post structure and style from retro-blog repository
     ☐ Fetch Cilium installation documentation from GitHub
     ☐ Create the blog post file with proper structure and content
     ☐ Add relevant links to existing content where possible

● Now let me fetch the Cilium installation documentation from GitHub:

● Fetch(https://github.com/cilium/cilium/tree/v1.17.4/install/kubernetes/)…
  ⎿  Received 179.6KB (200 OK)

● Let me try a more direct approach to get Cilium documentation:

● Fetch(https://docs.cilium.io/en/stable/installation/k8s-install-helm/)…
  ⎿  Received 79.9KB (200 OK)

● Update Todos
  ⎿  ☒ Examine existing blog post structure and style from retro-blog repository
     ☒ Fetch Cilium installation documentation from GitHub
     ☐ Create the blog post file with proper structure and content
     ☐ Add relevant links to existing content where possible

● Now I'll create the blog post file. First, let me check if the retro-blog directory exists:

● List(.)…
  ⎿  Listed 4 paths (ctrl+r to expand)

● I need to create the blog post file as specified. Based on the requirements, I should create it at retro-blog/content/view-network-policy-violations.md. Let me create this structure:

● Bash(mkdir -p retro-blog/content)…
  ⎿  (No content)

● Now I'll create the blog post file:

```

4. cost:
> /cost 
  ⎿  Total cost:            $0.67
     Total duration (API):  4m 37.4s
     Total duration (wall): 6m 9.8s
     Total code changes:    86 lines added, 0 lines removed
     Token usage by model:
         claude-3-5-haiku:  91.3k input, 1.3k output, 0 cache read, 0 cache write
            claude-sonnet:  127 input, 8.2k output, 552.5k cache read, 81.3k cache write


## Second try now in the folder rettor-blog:
> Create the blog post as described in BLOG_POST.md

● I'll create the blog post based on the description in BLOG_POST.md. Let me first read that    Cost: $0.0186 (3.9s)
  file to understand what needs to be created.

● Read(file_path: "/home/reuhl/git/github/retro-blog/BLOG_POST.md")…                            Cost: $0.0186 (3.9s)
  ⎿ ## Context: Blog entry
    ## Constraints
    * Allign any generated content with regards to style and structure with the already existing content
    * Create links to already existing content where possible
    * If possible try to relate the new content to already existing content and add links
    * Fetch any webpage necessary. For example: https://github.com/cilium/cilium/tree/v1.17.4/install/kubernetes/
    cilium

    ## Task
    Add a blog post in the file retro-blog/content/view-network-policy-violations.md for the task that I did which
    is described in brief here:
    ### Problem:
    * Currently using calico in current project
    * Finding it hard to detect network policy violations (not supported by calico out of the box)
    ### Idea
    * Use cilium which promises better observabiltiy per default
    * Currently newbie to cilium, aim to get thngs working fast
    ### Solution:
    * Deploy with helm using specific parameters:
        --set debug.verbose="flow policy kvstore envoy datapath" \
        --set hubble.dropEventEmitter.enabled=true \
        --set hubble.dropEventEmitter.interval=5s
    ### Test
    * Deployed manifests in cni-test (briefly describe)
    * Get the ip of one of the nginx pods: kubectl get pods -n cni-test -l app=nginx -o
    jsonpath='{.items[*].status.podIP}'
    * Run network troubleshooting Pod and try to access using curl:
    kubectl run -ti netshot --image=nicolaka/netshoot -n cni-test
    curl <pod-id> 80
    * Look at the events:
    kubectl get events -n cni-test --watch
    0s          Warning   PacketDrop          pod/netshot                  Outgoing packet dropped (policy_denied)
    to cni-test/nginx-5c754d96b-6r7x2 (10.0.0.226) TCP/80
    Success: Policy violations can be discovered by just looking at the events
    * Violations can also be viewd using "hubble":
    $ kubectl exec -ti -n kube-system cilium-7z4ct -c cilium-agent -- hubble observe -f --from-label run=netshot
    May 31 05:24:48.077: cni-test/netshot:47302 (ID:59296) <> cni-test/nginx-5c754d96b-6r7x2:80 (ID:2290)
    policy-verdict:none EGRESS DENIED (TCP Flags: SYN)
    May 31 05:24:48.077: cni-test/netshot:47302 (ID:59296) <> cni-test/nginx-5c754d96b-6r7x2:80 (ID:2290) Policy
    denied DROPPED (TCP Flags: SYN)
    Notet that for this the user must have priviliges to do an "exec" in the Pods in the namespace "kube-system"
    which might not be the case for managed clusters

    ### Conclustion
    * Write 2 to 3 sentences
    * Where to go from here: Next step is to trying to get more information about why the packages have been
    dropped. For example which policy / rules where violated


● Now I'll create a todo list to track this task, then examine the existing blog posts to       Cost: $0.0067 (9.6s)
  understand the style and structure.

● Update Todos                                                                                  Cost: $0.0067 (9.6s)
  ⎿  ☐ Analyze existing blog post structure and style (P0)
     ☐ Create the blog post file with proper frontmatter and content (P0)
     ☐ Fetch cilium GitHub page for reference links (P1)
     ☐ Find related network policy content to link to (P1)

● Update Todos                                                                                  Cost: $0.0103 (4.7s)
  ⎿  ☐ Analyze existing blog post structure and style (P0)
     ☐ Create the blog post file with proper frontmatter and content (P0)
     ☐ Fetch cilium GitHub page for reference links (P1)
     ☐ Find related network policy content to link to (P1)

● Let me examine some existing blog posts to understand the structure and style:                Cost: $0.0030 (7.0s)

● Read(file_path: "/home/reuhl/git/github/retro-blog/content/post/k8s-netwrok-policies.md")…    Cost: $0.0030 (7.0s)
  ⎿ +++
    author = "Thomas Reuhl"
    title = "Test probes using network policies"
    date = "2021-03-15"
    description = "How to use network policies to test health probes"
    tags = [
        "k8s"
    ]
    categories = [
        "k8s"
    ]
    series = ["k8s"]
    +++
    # How to use network policies to test health probes
    Recently I faced the problem how to test a [health
    probe](https://kubernetes.io/docs/tasks/configure-pod-container/configure-liveness-readiness-startup-probes/) of
     a container. To be more precise it was a liveness probe that would only succeed if the connection to its _on
    premise_ database was working.\
    There are a lot of options on how to test this probe; Adding a temporary firewall rule, blocking traffic on the
    database, and so forth.\
    Since these options all require modifications to external systems I opted for a pure Kubernetes approach by
    putting a [network policy](https://kubernetes.io/docs/concepts/services-networking/network-policies/) between
    the Pod and the database.

    ## Setting up the network policy
    Setting up the policy is straight forward. There some good examples for network policies in [this 
    repository](https://github.com/ahmetb/kubernetes-network-policy-recipes)\
    I used one that would generally block egress traffic from the Pod expect for DNS resolution requests:
    ```yaml
    apiVersion: networking.k8s.io/v1
    kind: NetworkPolicy
    metadata:
      name: deny-external-egress
      namespace: my-app-test
    spec:
      podSelector:
        matchLabels:
          app: my-app
      policyTypes:
      - Egress
      egress:
      - ports:
        - port: 53
          protocol: UDP
        - port: 53
          protocol: TCP
      - to:
        - namespaceSelector: {}
    ```
    Since the postgres database listens on port `5432` that traffic would be blocked. The `podSelector` makes sure
    that only the Pod `my-app` is affected.

    ## Test the test
    Shortly after applying the network policy the Pods started to get unhealthy and Kubernetes tried to restart
    them. Corresponding events appeared as well:
    ```bash
    $ kubectl get events -n my-app-test
    my-app-test  Warning   Unhealthy         pod/my-app-6c84dd4647-w5jjn     Liveness probe failed: HTTP probe
    failed with statuscode: 503
    my-app-test  Normal    Killing           pod/my-app-6c84dd4647-w5jjn  Container my-app failed liveness probe,
    will be restarted
    my-app-test  Warning   BackOff           pod/my-app-6c84dd4647-w5jjn  Back-off restarting failed container
    ```
    After removing the network policy, the Pods recovered and started to get healthy again.

    ## Conclusion
    Using network policies is an easy way to test liveness probes which evaluate connectivity to other components
    being it _in cluster_ or _on premise_. The main advantage being that no external system needs to be altered to
    do the test.\
    Using the same approach _resilience_ of an application to network outages can be tested.


● Search(pattern: "network.*polic", path: "/home/reuhl/git/github/retro-blog/content/post", …   Cost: $0.0030 (7.0s)
        include: "*.md")
  ⎿  Found 3 files
     /home/reuhl/git/github/retro-blog/content/post/sod/k8s-network-policy-viewer.md
     /home/reuhl/git/github/retro-blog/content/post/prometheus-test-alerts.md
     /home/reuhl/git/github/retro-blog/content/post/k8s-netwrok-policies.md

● Fetch(url: "https://github.com/cilium/cilium/tree/v1.17.4/install/kubernetes/cilium", …       Cost: $0.0030 (7.0s)
       prompt: "Extract information about cilium installation and network observability
       features, focusing on hubble and network policy debugging capabilities")
  ⎿  Received 492.2KB (200 OK)
Based on the Cilium Helm chart values, here are key insights about Cilium's installation and network observability
features:

Network Capabilities:
- Operates at Layer 3/4 for traditional networking and Layer 7 for modern protocols like HTTP, gRPC, and Kafka
- Uses eBPF technology for "dynamic insertion of eBPF bytecode into the Linux kernel"

Hubble Observability Features:
- Supports automatic certificate generation for network visibility
- Provides metrics and tracing capabilities
- Can generate events with configurable:
  - Aggregation levels
  - Monitoring intervals
  - TCP flag tracking

Network Policy and Debugging:
- Supports policy verdict events
- Enables drop event tracking
- Offers "trace events" for detailed network debugging

Key Technical Highlight:
"Cilium is open source software for providing and transparently securing network connectivity and loadbalancing
between application workloads"

The implementation leverages eBPF, which is described as "highly efficient and flexible" for implementing
networking, security, and visibility logic.

● Now let me check the network policy viewer and find related content:                          Cost: $0.0055 (7.4s)

● Read(file_path:                                                                       …       Cost: $0.0055 (7.4s)
      "/home/reuhl/git/github/retro-blog/content/post/sod/k8s-network-policy-viewer.md")
  ⎿ +++
    author = "Thomas Reuhl"
    title = "K8s: View network policies"
    date = "2022-08-10"
    draft = "true"
    description = "K8s: View network policies"
    tags = []
    categories = [
        "Snippet of the day"
    ]
    visibility = [
        "false"
    ]
    +++
    This snippet is not so much a snippet but rather a link to a very useful page with which you can evaluate
    kubernetes [network policies](https://kubernetes.io/docs/concepts/services-networking/network-policies/):

    [https://orca.tufin.io/netpol/](https://orca.tufin.io/netpol/)

    Since the structure of network policies is somewhat complicated, this tools is really nice since it detects
    syntax errors and outputs the content of a network policy in natural language. For example the following network
     policy:
    ```yaml
    apiVersion: networking.k8s.io/v1
    kind: NetworkPolicy
    metadata:
      name: apiserver-egress
      namespace: test
    spec:
      egress:
      - ports:
        - port: 6443
          protocol: TCP
        to:
        - namespaceSelector:
            matchLabels:
              name: kube-system
          podSelector:
            matchLabels:
              component: kube-apiserver
      podSelector:
        matchLabels:
          app.kubernetes.io/name: nginx-ingress-controller
      policyTypes:
      - Egress
    ```
    evaluates to the following description:
    ```
    Policy 1 - apiserver-egress
        Egress
            Allows pods in namespace test with labels app.kubernetes.io/name:
            nginx-ingress-controller to connect to pods with labels component:
            kube-apiserver in namespaces with labels name: kube-system on port TCP 6443
    ```
    Unfortunately it does not yet work vice versa ;-)

    _P.S.: The network policy above was intended to allow an nginx controller to connect to the api server. 
    Unfortunately this does not work with [selectors](https://stackoverflow.com/a/59016417) but only ip blocks..._

● Update Todos                                                                                  Cost: $0.0055 (7.4s)
  ⎿  ☒ Analyze existing blog post structure and style (P0)
     ☒ Fetch cilium GitHub page for reference links (P1)
     ☐ Find related network policy content to link to (P1)
     ☐ Create the blog post file with proper frontmatter and content (P0)

● Update Todos                                                                                  Cost: $0.0140 (5.4s)
  ⎿  ☒ Analyze existing blog post structure and style (P0)
     ☒ Fetch cilium GitHub page for reference links (P1)
     ☒ Find related network policy content to link to (P1)
     ☐ Create the blog post file with proper frontmatter and content (P0)

● Now I'll create the blog post file with the proper frontmatter and content:                  Cost: $0.0143 (35.1s)

● Write(/home/reuhl/git/github/retro-blog/content/post/view-network-policy-violations.md)…     Cost: $0.0143 (35.1s)
  ⎿  Wrote 105 lines to /home/reuhl/git/github/retro-blog/content/post/view-network-policy-violations.md
          +++
          author = "Thomas Reuhl"
          title = "Detecting Network Policy Violations with Cilium"
          date = "2025-02-06"
          description = "How to use Cilium's enhanced observability to detect and troubleshoot network policy
          violations"
          tags = [
              "k8s",
              "cilium"
          ]
          categories = [
              "k8s"
          ]
          series = ["k8s"]
          +++

          # Detecting Network Policy Violations with Cilium

          While working with Kubernetes [network 
          policies](https://kubernetes.io/docs/concepts/services-networking/network-policies/) in a current project
          using Calico, I encountered a significant limitation: detecting network policy violations is not supported
          by Calico out of the box. This made troubleshooting blocked connections extremely difficult.

          ## The Problem

          Network policies are essential for securing Kubernetes clusters, but when connections fail, it's often
          unclear whether the issue is due to:
          - Network policy restrictions
          - Application configuration
          - Service discovery problems
          - Infrastructure issues

          Without proper observability, debugging network connectivity becomes a time-consuming guessing game.

          ## The Solution: Cilium with Enhanced Observability

          [Cilium](https://github.com/cilium/cilium) promises better observability per default through its
          integration with Hubble and eBPF technology. To quickly get network policy violation detection working, I
          deployed Cilium using Helm with specific parameters that enable detailed network event tracking:

          ```bash
          helm install cilium cilium/cilium \
              --set debug.verbose="flow policy kvstore envoy datapath" \
              --set hubble.dropEventEmitter.enabled=true \
              --set hubble.dropEventEmitter.interval=5s
          ```

          These parameters enable:
          - **Verbose debugging**: Detailed logging for flow, policy, and datapath events
          - **Drop event emitter**: Automatic generation of Kubernetes events for dropped packets
          - **Event interval**: Configurable frequency for event generation (5 seconds)

          ## Testing the Setup

          To validate that network policy violations are properly detected, I deployed test manifests in a `cni-test`
           namespace and performed the following steps:

          1. **Get the IP of an nginx pod**:
             ```bash
             kubectl get pods -n cni-test -l app=nginx -o jsonpath='{.items[*].status.podIP}'
             ```

          2. **Run a network troubleshooting pod and attempt connection**:
             ```bash
             kubectl run -ti netshot --image=nicolaka/netshoot -n cni-test
             curl <pod-ip> 80
             ```

          3. **Monitor Kubernetes events for policy violations**:
             ```bash
             kubectl get events -n cni-test --watch
             ```

          ## Results

          The test was successful! When the curl command was blocked by a network policy, Cilium immediately
          generated a Kubernetes event:

          ```
          0s    Warning   PacketDrop    pod/netshot    Outgoing packet dropped (policy_denied) to
          cni-test/nginx-5c754d96b-6r7x2 (10.0.0.226) TCP/80
          ```

          This event clearly indicates:
          - The source pod (`netshot`)
          - The destination pod (`nginx-5c754d96b-6r7x2`)
          - The reason for the drop (`policy_denied`)
          - The destination IP and port

          ## Advanced Debugging with Hubble

          For even more detailed analysis, Cilium's Hubble provides granular network flow information:

          ```bash
          kubectl exec -ti -n kube-system cilium-7z4ct -c cilium-agent -- hubble observe -f --from-label run=netshot
          ```

          This command outputs detailed flow information:
          ```
          May 31 05:24:48.077: cni-test/netshot:47302 (ID:59296) <> cni-test/nginx-5c754d96b-6r7x2:80 (ID:2290)
          policy-verdict:none EGRESS DENIED (TCP Flags: SYN)
          May 31 05:24:48.077: cni-test/netshot:47302 (ID:59296) <> cni-test/nginx-5c754d96b-6r7x2:80 (ID:2290)
          Policy denied DROPPED (TCP Flags: SYN)
          ```

          **Note**: Hubble access requires exec privileges on pods in the `kube-system` namespace, which might not be
           available in managed Kubernetes clusters.

          ## Conclusion

          Cilium's enhanced observability significantly improves the debugging experience for network policy
          violations. The automatic generation of Kubernetes events provides immediate feedback when connections are
          blocked, eliminating much of the guesswork involved in network troubleshooting.

          For organizations struggling with network policy debugging, migrating from Calico to Cilium can provide
          substantial operational benefits. The next step would be to explore deeper policy analysis to understand
          which specific rules are causing violations.

          ## Related Posts

          - [Test probes using network policies](/post/k8s-netwrok-policies/) - Learn how to use network policies for
           testing application resilience
          - [View network policies](/post/sod/k8s-network-policy-viewer/) - Tools for visualizing and understanding
          network policy configurations

● Update Todos                                                                                  Cost: $0.0151 (5.3s)
  ⎿  ☒ Analyze existing blog post structure and style (P0)
     ☒ Create the blog post file with proper frontmatter and content (P0)
     ☒ Fetch cilium GitHub page for reference links (P1)
     ☒ Find related network policy content to link to (P1)

● Blog post created successfully at                                                             Cost: $0.0101 (2.9s)
  /home/reuhl/git/github/retro-blog/content/post/view-network-policy-violations.md. The post
  follows the existing style and structure, includes links to related network policy content,
   and covers all the technical details from the original task description.


---
Next: Try claude in retro-blog and set mcp to point to fleet-infra folder