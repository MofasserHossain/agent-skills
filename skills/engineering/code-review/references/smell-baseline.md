# Smell baseline

Code smells from Martin Fowler's *Refactoring* (chapter 3). The Standards axis checks them even when a project documents nothing. Each one is a judgement call ("possible Feature Envy"), never a hard violation, and a documented project standard that endorses the pattern suppresses it. Match each smell against the diff: what it is → how to fix it.

- **Mysterious Name**: a name that doesn't reveal what the thing does or holds. → Rename it; if no honest name comes, the design is murky.
- **Duplicated Code**: the same logic shape in more than one hunk or file. → Extract the shared shape and call it from both places.
- **Feature Envy**: a function that uses another object's data more than its own. → Move it to the data it envies.
- **Data Clumps**: the same few fields or parameters always travel together. → Bundle them into one type.
- **Primitive Obsession**: a primitive or string standing in for a domain concept. → Give the concept its own small type.
- **Repeated Switches**: the same switch or if-cascade on the same type in several places. → Use polymorphism, or one map that every site shares.
- **Shotgun Surgery**: one logical change forces scattered edits across many files. → Gather what changes together into one module.
- **Divergent Change**: one module edited for several unrelated reasons. → Split it so each part changes for one reason.
- **Speculative Generality**: abstractions, parameters or hooks for needs the spec doesn't have. → Delete them until a real need appears.
- **Message Chains**: long `a.b().c().d()` navigation that the caller shouldn't depend on. → Hide the walk behind one method.
- **Middle Man**: a class or function that mostly delegates onward. → Remove it and call the real target directly.
- **Refused Bequest**: a subclass that ignores or overrides most of what it inherits. → Replace the inheritance with composition.

Adapted from the `code-review` skill in mattpocock/skills (MIT).
