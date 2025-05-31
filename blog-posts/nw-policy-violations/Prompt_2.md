tom1299: ## Context: Blog entry
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

GitHub Copilot: I'll help you create a blog post about enabling network policy violation visibility with Cilium. Let me first explore the existing blog content to understand the style and structure, then create the new post. I see the file already exists. Let me read a few existing blog posts to understand the style and structure: Now let me check if the target file already exists and what content it has: Perfect! The file exists but is empty. Let me also check if there's a cni-test directory mentioned in the task to understand the testing setup: Now let me look for the calico-test directory mentioned in the task: Now let me search for the calico-test directory to understand the setup: Let me examine these test files to understand the setup: Now let me also fetch the Cilium GitHub page to understand the helm installation parameters mentioned in the task: Now I'll create the blog post with the content based on the task description and align it with the existing blog style I observed. The blog should be named `view-network-policy-violations.md` based on the task. Summarized conversation historyI'll help you create the blog post about enabling network policy violation visibility using Cilium. Let me first check the current state of the target file and gather some context about the existing blog structure. Now let me gather the context from the existing blog posts and technical setup to create the blog post: 

Continue to iterate?
Copilot has been working on this problem for a while. It can continue to iterate, or you can send a new message to refine your prompt.

tom1299: @agent Continue: "Continue to iterate?"

GitHub Copilot: I'll continue by creating the blog post content. Let me gather a bit more context from the existing blog structure and then create the complete blog post. Now let me find the Cilium installation section from the install script: Perfect! Now I have all the context I need. Let me create the complete blog post about enabling network policy violation visibility using Cilium: 
```


Made changes.


```
Perfect! I've successfully created the blog post about enabling network policy violation visibility using Cilium. The blog post includes:

## Key Features of the Blog Post:

1. **Proper Hugo frontmatter** - Following the existing blog structure with author, title, date, tags, categories, and series
2. **Technical content** - Detailed explanation of the problem with network policy observability and how Cilium solves it
3. **Specific Helm installation command** - Based on the actual configuration from your install.sh script with the debug parameters
4. **Testing methodology** - References to the existing calico-test manifests for practical testing
5. **Cross-references** - Links to existing blog posts like k8s-netwrok-policies.md and `sod/k8s-network-policy-viewer.md`
6. **Code examples** - Bash commands for installation, testing, and observing violations
7. **Best practices** - Production considerations for enabling debug features

## Technical Accuracy:

- Uses the exact Helm parameters from your install.sh
- References the actual test manifests in calico-test
- Follows the writing style and structure of your existing blog posts
- Includes proper explanations of the key debug parameters for policy violation visibility

The blog post is now ready and follows your existing blog's style and technical approach while providing valuable content about transitioning from Calico to Cilium for better network policy observability.