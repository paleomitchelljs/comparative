"""The joint graph: which joints a muscle spans, given its attachments.

Joints are edges in a graph whose nodes are bones, so the joints a muscle
crosses follow from where it attaches and never need asserting. Shared by
`validate.py` (to check stated actions against it) and `seed_actions.py` (to
correct a parse against it), because three copies of a graph traversal is two
too many — `assets/skeleton.js` holds the third, for the browser.

Two kinds of joint are edgeless and must be exempted from any "does this muscle
span it" test:

  serial    — both sides name the same element (intervertebral,
              interphalangeal). A long digital flexor reaches the
              interphalangeal joints through the metacarpophalangeal joint, so
              spanning is not the right question.
  parallel  — the two elements of one limb segment (radioulnar, tibiofibular).
              The biceps supinates by rotating the radius against the ulna
              while attaching only to the radius, so a span test would call a
              correct action wrong.
"""

from collections import deque


def build(joints_doc, elements_by_id):
    return JointGraph(joints_doc, elements_by_id)


class JointGraph:
    def __init__(self, joints_doc, elements_by_id):
        self.joints = {j["id"]: j for j in joints_doc["joints"]}
        self.elements = elements_by_id
        self.adj: dict[str, list[tuple[str, str]]] = {}

        self.exempt = set()
        for j in joints_doc["joints"]:
            prox = {r.get("element") for r in j.get("proximal", [])}
            dist = {r.get("element") for r in j.get("distal", [])}
            crossing = j.get("crossing", "serial" if prox == dist else "chain")
            if crossing != "chain":
                self.exempt.add(j["id"])
            for a in prox:
                for b in dist:
                    if not a or not b or a == b:
                        continue
                    self.adj.setdefault(a, []).append((b, j["id"]))
                    self.adj.setdefault(b, []).append((a, j["id"]))

    def node(self, element_id):
        """Walk up `partOf` to the nearest bone the graph knows about, so an
        attachment on the deltopectoral crest resolves to the humerus."""
        cur, guard = element_id, 0
        while cur and guard < 20:
            if cur in self.adj:
                return cur
            cur, guard = self.elements.get(cur, {}).get("partOf"), guard + 1
        return None

    def between(self, a_el, b_el):
        """The joints on the shortest path between two bones."""
        a, b = self.node(a_el), self.node(b_el)
        if not a or not b or a == b:
            return []
        prev, queue = {a: None}, deque([a])
        while queue:
            cur = queue.popleft()
            if cur == b:
                break
            for nxt, jid in self.adj.get(cur, []):
                if nxt in prev:
                    continue
                prev[nxt] = (cur, jid)
                queue.append(nxt)
        if b not in prev:
            return []
        out, cur = [], b
        while prev.get(cur):
            out.append(prev[cur][1])
            cur = prev[cur][0]
        return out

    def spanned_by(self, attachments):
        """Every joint spanned by one {origin: [...], insertion: [...]} block."""
        att = attachments or {}

        def ends(side):
            # A row may end on another muscle rather than a bone, in which case
            # it names no element and cannot place the muscle across a joint.
            # Those rows are skipped rather than contributing a None node.
            return {end for r in att.get(side, []) if isinstance(r, dict)
                    for end in [r.get("landmark") or r.get("element")] if end}

        out = set()
        for o in ends("origin"):
            for i in ends("insertion"):
                out.update(self.between(o, i))
        return out

    def permits(self, joint_id, motion):
        return motion in self.joints.get(joint_id, {}).get("motions", [])
