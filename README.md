A little live [Markdown][] previewer with almost no features. It renders Markdown
to HTML using [Pandoc][].

# Instructions

    % ./bin/markgown-preview

Open some Markdown file, and then try editing it in your text editor of choice.
Later, you can export the HTML if you like, or publish your Markdown source in
your normal way.

![](http://willthompson.co.uk/misc/markgown-preview.png)

# Questions nobody has asked

## Do you know about [gedit-markdown][]?

I do now. But I don't use `gedit`.

## What happened to the editor?

The code is still lying around, but why not use a real text editor? The only real benefit of a built-in editor was that you didn't need to save the document to have it refreshed, but you can get pretty close in Vim with:

```vimL
:au FocusLost * :wa
```

## Who wrote the beautiful CSS?

That would be [Kevin Burke][markdowncss]. Cheers!

[Markdown]: http://daringfireball.net/projects/markdown/
[Pandoc]: http://johnmacfarlane.net/pandoc/
    "I love horses. Best of all the animals"
[gedit-markdown]: http://www.jpfleury.net/en/software/gedit-markdown.php
[markdowncss]: http://kevinburke.bitbucket.org/markdowncss/
