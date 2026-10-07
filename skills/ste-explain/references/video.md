# Video mode

A short animation makes the reader watch an idea change step by step. It also forces you to decide what occurs next, which shows gaps in the explanation. The video is silent by default: the text on screen tells the story.

This mode needs a place to run code (Python and ffmpeg). If you cannot run code, write the script and the storyboard, and tell the user how to render them.

## What to produce

1. A storyboard: a numbered list of scenes, one STE sentence for each scene. Show it to the user first if the topic is large.
2. A Manim script. Start from `assets/manim_template.py`.
3. The rendered MP4, plus the script, so that the user can read and change each claim.

## Tools

- Use Manim Community Edition (`pip install manim`). It is the community version of the engine that the 3Blue1Brown channel uses.
- Manim needs the system libraries cairo and pango, and ffmpeg. On Debian or Ubuntu: `apt-get install libcairo2-dev libpango1.0-dev ffmpeg`. On macOS: `brew install cairo pango ffmpeg`.
- Do not use `Tex`, `MathTex`, `DecimalNumber` or number labels on axes unless LaTeX is installed. These classes need LaTeX. Use `Text` for all words and numbers. The template does this.
- If the install fails on the newest Python, make a virtual environment with Python 3.11 or 3.12.

## Style

- Dark background, a small palette (one blue, one yellow accent, one red, one green), smooth transforms.
- Do not copy another creator's characters, logos or mascots. The style is the calm pace and the clear motion.
- One idea in each scene. Remove the previous scene before the next one starts.
- Text size: at least 24 for captions and 30 for main text at 1080p. A phone must show it clearly.
- Text on screen follows the STE rules. Maximum two short sentences on screen at one time.
- Show change with motion: grow a bar, move a dot along an arrow, fade the old word and show the new word in the accent colour.
- Hold each finished frame for 2 to 3 seconds so that the viewer can read it.

## Research and sources

For a factual topic, follow `research.md` first and write the storyboard from the fact list. Make the last scene show the names of the sources for 3 seconds. Put the full URLs in a comment at the top of the script and in your message to the user. Do not put a long URL on the screen.

## Length

- 60 to 120 seconds. 6 to 9 scenes.
- The first scene gives the question. The last scene gives the answer in one sentence, and the limit of the explanation if there is one.

## Render

```bash
manim -ql scene.py Explainer                      # fast preview, 480p
manim --resolution 1920,1080 --fps 30 scene.py Explainer   # final
```

After the preview, extract a few frames and look at them. Check for text that goes off the screen and for objects that overlap.

```bash
ffmpeg -i media/videos/scene/480p15/Explainer.mp4 -vf "fps=1/5,scale=640:-1,tile=3x4" -frames:v 1 sheet.png
```

## Narration

Add a voice only if the user asks for one.

- Write the narration as a text file first. The user must be able to read it.
- Use a local text-to-speech tool if one is available. If the user wants a hosted service, they must supply the key as an environment variable. Do not ask the user to paste a key into the chat.
- Tell the user that a hosted service receives the narration text. Keep private material out of it.

## Before you deliver

- Check each number and each claim in the script against the source. An incorrect claim in an animation is harder to see than an incorrect sentence.
- Give the script with the video.
