# Logic prototype

One self-contained HTML file, a **shareable demo**, that lets anyone (a non-developer included) drive a state model by clicking buttons. Use it for business logic, state transitions or data shape: things that look reasonable on paper but feel wrong once real cases push through them.

1. **State the question** in a visible intro at the top of the page: the state model, and the question it tests.
2. **Isolate the logic** in one `<script>` block, written as a small pure module that could be lifted into the real codebase. Choose the shape that fits the question:
   - a reducer, `(state, action) => state`, for discrete events;
   - an explicit state machine, when "which actions are legal right now" is part of the question;
   - pure functions over plain data, when there is no current state;
   - a class with a clear method surface, when the logic genuinely owns ongoing state.
   The module never touches the DOM. The page calls into it, and nothing flows back.
3. **Build the page** in plain HTML, CSS and JS, all inline, with no framework, bundler or server, so it opens with a double-click and survives being emailed. Write every label in the domain's language, not the code's. From top to bottom:
   - a title and a one-line explanation;
   - the **current state**, shown as labelled fields rather than raw JSON, re-rendered after every click, with the change called out;
   - **free-play buttons**, one per action, always available;
   - **guided walkthroughs**, one tab per scenario: the happy path, a tricky edge case, and an attempt at something that should be illegal. Each starts from a known state, and its steps are real buttons.
   Keep the design clean and restrained: readable type, generous spacing, one accent color, no animation.
4. **Hand it over.** The valuable moments are "wait, that shouldn't be possible": bugs in the idea itself. Add actions or scenarios when they ask.
5. **Capture.** The validated module lifts into the real code. The HTML shell goes to the throwaway branch, where it stays runnable.

Adapted from the `prototype` skill in mattpocock/skills (MIT).
