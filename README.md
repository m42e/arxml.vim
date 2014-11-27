arxml.vim
=========
[![Gitter](https://badges.gitter.im/Join Chat.svg)](https://gitter.im/m42e/arxml.vim?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)
Provides a more usefull folding for AUTOSAR XML files (arxml).
It shows the shortname of the collapsed element in the foldtext, and shows the subpackages of ar-packages elements.
And it allows to jump to the the linked reference using: ```call FollowShortName()```

Dependencies
========
- vim must be compiled with python support
- lxml must be instlled for python

TODO
========
- ~~It would be most usefull if somehow a linking of the shortnames to the specific elements can be performed using xpath.. maybe the xpath plugin is helpfull here~~
- ~~Add optional shortcut to jump to shortname location (this only works in the current file, and is not planned to be extended in near future)~~
- more special handlings of some elements
- ~~documentation~~
