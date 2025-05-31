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
