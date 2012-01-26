# Markgown

A [wjt](http://wjt.me.uk/) production.

## Introduction

This is a *really stupid* Markdown editor with **live preview**. It might be useful if you *hate your data*; but it also might be useful if you want a __distraction-free Markdown editing experience__!

## How do I use it?

Launch it:[^1]

    % touch my-document.md
    % markgown my-document.md

And then mash on your keyboard. The preview will be updates as and when it feels like it. It will probably lose your position when it does so. The document is saved whenever the preview updates. If the spinner is spinning in the corner, you have unsaved changes. If it's not, you can quit with impunity.

[^1]: the file has to exist before you start editing.

## How does it work?

It uses `GtkSourceView` on the left hand side, and a WebKit view on the right-hand side, both from Python using GObject introspection. Behind the scenes it uses [Pandoc][]. So we have:

* C;
* Python;
* Haskell;
* and a dormant JavaScript engine.

This is the future!

## Do you know about [gedit-markdown][]?

Yes.

[Pandoc]: http://johnmacfarlane.net/pandoc/s
    "I love horses."
[gedit-markdown]: http://www.jpfleury.net/en/software/gedit-markdown.php