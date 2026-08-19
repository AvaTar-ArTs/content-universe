export const STATUSES = ["observed","modeled","available","executed","verified","blocked"];
export const VERBS = ["CREATE","REFINE","AUTOMATE","SHARE","PROTECT","PUBLISH","EVALUATE","DERIVE","REFERENCES"];
export const OPERATIONS = ["create","edit","remix","reframe","upscale","describe"];

export function assertWorkflowGraph(graph) {
  if (!graph || typeof graph.id !== "string" || typeof graph.version !== "string") {
    throw new Error("workflow graph requires id and version");
  }
  const ids = new Set();
  for (const node of graph.nodes ?? []) {
    if (!node || typeof node.id !== "string" || ids.has(node.id)) {
      throw new Error("workflow graph contains a missing or duplicate node id");
    }
    ids.add(node.id);
    if (!STATUSES.includes(node.status)) throw new Error(`invalid node status: ${node.status}`);
  }
  for (const edge of graph.edges ?? []) {
    if (!ids.has(edge.source) || !ids.has(edge.target)) throw new Error("edge references unknown node");
    if (!VERBS.includes(edge.verb)) throw new Error(`invalid workflow verb: ${edge.verb}`);
  }
  return graph;
}

export function normalizeBBox([yMin,xMin,yMax,xMax]) {
  if (![yMin,xMin,yMax,xMax].every(Number.isFinite) || yMax < yMin || xMax < xMin) {
    throw new Error("invalid Ideogram bbox");
  }
  return {x:xMin,y:yMin,width:xMax-xMin,height:yMax-yMin};
}

export function toIdeogramBBox({x,y,width,height}) {
  if (![x,y,width,height].every(Number.isFinite) || width < 0 || height < 0) {
    throw new Error("invalid neutral bbox");
  }
  return [y,x,y+height,x+width];
}

export function createManifest(intent, elements = []) {
  return {id:`manifest-${Date.now()}`,version:"0.1.0",intent,scene:{elements},lineage:{parent_ids:[]}};
}
