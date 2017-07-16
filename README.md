# git-tickets

This repository contains a spec to track tickets (bugs, pull-requests, …) in a
plain text format within a git repository.


## Spec

Tickets are tracked in a dedicated branch named "tickets".

The "tickets" branch contains one file per ticket. The filenames are
incrementing numbers starting with 1. There are no other files or directories
in the "tickets" branch.

A ticket file is a minimal [mbox]-like file. Metadata is encoded as headers in
the first message:

-	`Subject`: The title of the ticket [required]
-	`Author`: The author of the ticket (probably the same as mentioned in the
	`From_` line) [requried]
-	`State`: Either "open", "closed", or some custom value [default: "open"]
-	`Assignee`: The person this ticket is assigned to
-	`Labels`: A comma-separated list of labels (e.g. "bug", "duplicate",
	"wontfix")
-	`Branch`: Associate this ticket with the given branch, making this a
	pull-request

Headers SHOULD be capitalized.  They SHOULD NOT be folded to allow simple
line-based operations on them.  The `Orig-Date` and `From` headers SHOULD be
omitted.

Any subsequent messages ("comments") SHOULD NOT contain any of these headers.
Messages SHOULD be separated with two blank lines.

The body of a messages SHOULD use the [commonmark] format.

Commit messages related to tickets SHOULD conform to the general format
`{Action} #{Number} [- {Title}]`, e.g. `Open #12 - Add mail support`.


## Example ticket file

	From someone@example.com Mon Jul 17 13:00:00 2017
	Subject: Add mail support
	Author: someone@example.com
	State: closed
	Labels: enhancement,wontfix

	If it ain't got mail support, I won't use it!


	From xi@example.com Tue Jul 18 14:00:00 2017

	It was a design decision to not do this. Closing as wontfix.


## Tooling

-	Run `git checkout --orphan tickets` to create the "tickets" branch.
-	Run `git fetch origin tickets && git diff tickets origin/tickets` to see what
	changed since your last pull.
-	Run `mutt -R -f {ticket}` to read the conversation in [mutt].
-	The script `git-tickets` included in this repository is useful to filter and
	list tickets. It will only list open tickets by default.
-	The script `import-github.py` included in this repository can be used to
	import issues and pull-requests from github.
-	If you are using gitolite, add the line `RW tickets = @all` to a repo's
	config in order to allow people to create tickets.


## Design and Reasoning

The main idea behind the design is simplicity. This is expressed on different
levels:

-	No tools other than git and a text editor should be required.
-	Additional (optional) tools should be simple to create and use.
-	The structures are very much inspired by github, notably:
	-	linear discussions
	-	customizable labels instead of complex taxonomies
	-	ticket IDs are incrementing numbers
	-	formatting with commonmark
	-	simple references to tickets, users, and code [not yet done]


## FAQ

### `ls` just shows me a list of numbers. How am I supposed to find relevant tickets?

This format was chosen so that conflicts are automatically detected by git. It
is true that it is somewhat ugly though. This is why I wrote the `git-tickets`
script.

### I can change old messages, even by other people! That must be a bug, right?

This is actually intentional. In the case of metadata, this is even the only
way to do it.

Sometimes people create badly formatted (or even invalid) tickets. And of
course there is the problem of spam. There could be a sophisticated moderation
system, but just editing plain text files is so much simpler.

Also note that any changes can be tracked in the git history.

### How can I edit code and tickets at the same time.

This is a clear disadvantage of this approach: You cannot easily switch
between regular code and the "tickets" branch. You can have a second clone of
the repo though.

### Using git for authentication is a high barrier for reporters.

Yes and no.

Many people who write bug reports or pull requests know git. Other people
typically prefer other means of communication, e.g. support forums.

Still, adding an ssh-key to a repo is some work. Not much more work than
subscribing to a mailing list, but still a lot to ask for just fixing a typo.

### Why is there no email support

Just as plain text files and git, mail is another system that developers
use on a daily basis. However, I did not want to require an additional server.

Additionally, mail is a baroque system with many options. I did not want to
deal with HTML-email, MIME, encryption, different encodings, ….

### Why are there no threaded discussions? Even github has them!

Github does not have threaded discussions in general. However, you can comment
code lines in pull requests, which results in something very similar to
threads.

Unfortunately, it is quite hard to represent threads in a human readable plain
text file. You may use the `In-Reply-To` header, but I believe that extensive
quoting should be sufficient for most cases.

### When the zombie apocalypse starts and the github engineers are among the first victims (god behold!) and github goes down immediately, will this be our saviour?

Yes.

### How does git-tickets compare to github?

git-tickets is very much inspired by the ticket system on github. However,
there are some key differences:

-	[github] is much more than a ticket system and offers (among other things)
	hosting, a web interface, permission management, and project discovery.
-	A web interface is used instead of editing plain text files.
-	A separate authentication system is used.
-	Github is a single point of failure. You cannot easily migrate to another
	hoster.

### How does git-tickets compare to mailing lists?

Mailing lists have been around for decades. They are still very much in use for
sending in patches and discussing code. Archives allow to publicly reference
these discussions.

Similar to git-tickets, this workflow relies on established protocols and
free-text communication. But there are some important differences:

-	No ticket-specific filters.
-	Tools do not implicitly know about the code that is discussed.
-	A separate authentication system is used.
-	A separate server is needed.

### How does git-tickets compare to debbugs?

[debbugs] is basically a mailing list optimized for tickets. It solves the
issue of filtering tickets. The other differences still apply.

### How does git-tickets compare to bugseverywhere?

[bugseverywhere] is a project with goals very similar to this one. It already
has a rich ecosystem of tools. Main differences:

-	It stores the tickets in the same branches as code. This has some cool
	properties, but also adds complexity. This also means that you need full
	write access to create a ticket.
-	A command line tool is used instead of editing plain text files.

### How does git-tickets compare to fossil?

[fossil] is a CVS like git, but it comes with a ticket system, a web server,
and a wiki included. Main differences:

-	Not compatible with other versioning systems (e.g. git)
-	A command line tool is used instead of editing plain text files.


[mbox]: https://tools.ietf.org/html/rfc4155
[commonmark]: https://spec.commonmark.org/
[github-refs]: https://help.github.com/articles/autolinked-references-and-urls/

[suckless]: http://lists.suckless.org/dev/1201/10574.html
[RFC 1297]: https://tools.ietf.org/html/rfc1297

[github]: https://github.com/
[sit]: https://github.com/maandree/sit
[fossil]: https://www.fossil-scm.org/index.html/doc/trunk/www/bugtheory.wiki
[bugseverywhere]: http://www.bugseverywhere.org/
[debbugs]: https://bugs.debian.org/debbugs-source/mainline/README.md

[stagit]: https://git.2f30.org/stagit/
[tig]: https://jonas.github.io/tig/
[tig-feature-request]: https://github.com/jonas/tig/issues/299
[mutt]: http://www.mutt.org/
