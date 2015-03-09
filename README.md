# Markgown

A [wjt](http://wjt.me.uk/) production.

## Introduction

This is a *really stupid* [Markdown][] editor with **live preview**. It might be useful if you *hate your data*; but it also might be useful if you want a __distraction-free Markdown editing experience__!

(Of course, distraction-free is relative if you find yourself hacking on a distraction-free editor when you're supposed to be doing something else…)

![Just a screenshot](http://willthompson.co.uk/misc/markgown.png)

## How do I use it?

Launch it on an existing file:

    % touch my-document.md
    % markgown my-document.md

And then mash on your keyboard. The preview will be updates as and when it feels like it. The document is saved whenever the preview updates, and also when you close the window.

Or if you just want a live preview:

    % markgown-preview my-document.md

## How does it work?

It uses `GtkSourceView` on the left hand side, and a WebKit view on the right-hand side, both from Python using GObject introspection. Behind the scenes it uses [Pandoc][]. So we have:

* C;
* Python;
* Haskell;
* and a dormant JavaScript engine.

This is the future!

## Do you know about [gedit-markdown][]?

Yes, but this is more fun for me.

## Would you like the pips’ background to be the same as the background of the GtkSourceView?

Yes, that would be lovely. But I can't figure out how to make that happen. I'm not very smart.

## Are the pips really preferable to a spinner?

Yeah. I mean, ideally, it would be a circle from which a segment is removed every second or something but that would require faffing around with Cairo so I didn't bother.

## Who wrote the beautiful CSS?

That would be [Kevin Burke][markdowncss]. Cheers!

[Markdown]: http://daringfireball.net/projects/markdown/
[Pandoc]: http://johnmacfarlane.net/pandoc/
    "I love horses. Best of all the animals"
[gedit-markdown]: http://www.jpfleury.net/en/software/gedit-markdown.php
[markdowncss]: http://kevinburke.bitbucket.org/markdowncss/
