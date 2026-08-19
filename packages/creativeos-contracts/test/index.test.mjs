import test from "node:test";
import assert from "node:assert/strict";
import {assertWorkflowGraph, normalizeBBox, toIdeogramBBox} from "../src/index.mjs";

test("validates workflow graph references and status", () => {
  const graph = {
    id:"workflow.demo", version:"0.1",
    nodes:[{id:"brief", status:"observed"}, {id:"manifest", status:"modeled"}],
    edges:[{source:"brief", verb:"CREATE", target:"manifest"}]
  };
  assert.equal(assertWorkflowGraph(graph), graph);
});

test("rejects duplicate nodes and dangling edges", () => {
  assert.throws(() => assertWorkflowGraph({
    id:"bad", version:"0.1",
    nodes:[{id:"a",status:"observed"},{id:"a",status:"modeled"}], edges:[]
  }));
  assert.throws(() => assertWorkflowGraph({
    id:"bad", version:"0.1",
    nodes:[{id:"a",status:"observed"}], edges:[{source:"a",verb:"CREATE",target:"missing"}]
  }));
});

test("converts Ideogram bbox order without losing geometry", () => {
  const neutral = normalizeBBox([0.1,0.2,0.7,0.9]);
  assert.deepEqual(neutral, {x:0.2,y:0.1,width:0.7,height:0.6});
  assert.deepEqual(toIdeogramBBox(neutral), [0.1,0.2,0.7,0.9]);
});
