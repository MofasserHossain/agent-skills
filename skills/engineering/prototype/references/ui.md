# UI prototype

Several **radically different** variations on one route, switched with a floating bar, so the user can flip between them and pick one, or combine parts of several.

## Where it lives

**Prefer an existing page.** Render the variants on the page that will host the feature, gated by a `?variant=` search parameter, and keep that page's real data fetching, auth, header and density. A design judged on an empty page hides the problems a populated one would show. Only when nothing could host the feature, create a throwaway route that follows the project's routing convention and has "prototype" in its path.

## Steps

1. **Write the plan in one line** at the top of the file, for example: "Three variants of the settings page, switchable via `?variant=`, on `/settings`." Default to three variants and never exceed five.
2. **Draft structurally different variants.** They differ in layout, information hierarchy and primary action, not in color. Each uses the project's component and styling system and exports a clear name (`VariantA`). If two come out alike, redo one with an explicit constraint such as "no card grid". Variants may share a small piece like the header, never the layout.
3. **Wire one switcher** on the route. It reads `?variant=` (default `A`) and renders the matching variant below the existing data fetching.
4. **Build the floating bar** as one shared component, fixed at the bottom center:
   - ← and → arrows cycle through the variants, wrapping at the ends;
   - a label shows the key and the variant's name, for example `B (Sidebar layout)`;
   - the arrows update the URL through the framework's router, so a variant is shareable and survives a reload;
   - the keyboard arrows also cycle, except while an input, textarea or editable element has focus;
   - it is styled to look unmistakably separate from the design, and hidden in production builds.
5. **Keep the variants read-only**, and point any mutation at a stub. The question is what the page should look like, not whether the backend works.
6. **Hand over** the URL and its variant keys. The real answer is often "the header from B with the sidebar from C".
7. **Capture.** Record which variant won and why. Fold the winner into the real page, rewritten properly, because prototype code skipped tests and error handling. Move the full set of variants and the switcher to the throwaway branch and out of main.

Adapted from the `prototype` skill in mattpocock/skills (MIT).
