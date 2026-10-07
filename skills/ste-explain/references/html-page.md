# Page mode

An interactive page lets the reader change an assumption and see the result. That is what a page can do and prose cannot. A page that only shows styled text is not worth the extra time.

## What to produce

One self-contained HTML file. Start from `assets/explainer-template.html` and replace its content.

If the surface has its own page or artifact tool, use that tool and follow its rules for the document skeleton. Otherwise save the file and give it to the user.

## Research first

If the topic is factual and the surface has web tools, follow `research.md` before you build the page. Build the page from the fact list. Every number on the page must come from the fact list. If the surface has no web tools, build the page from what you know, leave out the "Sources" section, and say in the page footer that the facts are not checked.

## Rules

1. **One file.** Inline all CSS and JavaScript. Do not load a framework for a small page. Do not load remote images.
2. **All text on the page follows the STE rules** in `SKILL.md`.
3. **At least one control changes an assumption.** A slider, a toggle or a step button. The reader must see the output change. Good: "Change the cache time and see how many requests reach the server." Not useful: a button that only shows hidden text.
4. **Animate the mechanism.** The page must have at least one animated diagram or chart that shows the process, not only the result. Use inline SVG with a small script. Examples: a dot that travels along an arrow, a bar that grows, a state that lights up in turn. Rules for the animation:
   - It shows the same model as the control. When the reader moves the slider, the animation changes with it.
   - It has a Pause button and a Play button (one toggle is fine), and the button is a real `button`.
   - It starts paused when `prefers-reduced-motion: reduce` is set.
   - It has a `title` and a `desc` in the SVG, so a screen reader gets the meaning.
   - It does not flash. It moves slowly enough to follow.
   - `assets/explainer-template.html` has a working example. Replace its labels and its model.
5. **List the assumptions on the page.** Use a visible section with the title "Assumptions". Include each simplification that the model in the page makes.
6. **The page is complete when it opens.** Show a realistic starting state. Do not show an empty screen that waits for input.
7. **It works on a phone.** One column below 600 px. No horizontal scroll of the page body.
8. **It works in light and dark themes.** Define colours as CSS variables and give dark values under `prefers-color-scheme: dark`.
9. **It works with a keyboard.** Use real `button`, `input` and `label` elements. Keep a visible focus outline.
10. **Motion has a purpose.** Animate the thing that changes. Respect `prefers-reduced-motion`.

## Structure that works

1. Title and one-sentence answer.
2. The interactive part, near the top.
3. The animated diagram.
4. A short explanation in STE.
5. Assumptions.
6. Sources. See below.

## The Sources section

- Make an ordered list. Each item is a real link: `<a href="..." target="_blank" rel="noopener noreferrer">`. Show the title, the site name, the date of the page if it shows one, and the date that you read it.
- Add one short line for each item that says which claim it supports. In the text, put the item number in brackets after the claim, for example `[2]`, and link it to the item.
- Cite only pages that you opened in this session. Copy each URL exactly. Do not guess a URL. Do not add a link only to make the list longer.
- Show the full URL as the link text, or in a `title` attribute, so that the reader sees where the link goes.
- If two sources disagree, show both values on the page and say which source gives which value.
- Add one line: "A link shows where a claim came from. It does not prove that the claim is true."

## Tell the user the limit

The page shows your model of the subject. It does not test the real system. If the page explains a bug, the user must still reproduce the bug with the real code. Say this in one sentence when you deliver the page.

## Before you deliver

- Open the page if you can, and use each control once.
- Check the page at a width of 400 px.
- Check that each number on the page comes from the script, or from a source that you name.
- Open each link once, or at least check that each URL is the same as the one that you opened during research.
- Use the Pause button, then the Play button. Move the slider, and check that the animation changes.
