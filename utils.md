# Keynote & code highlighting

```shell
pygmentize -f rtf -O "fontface=Monaco,fontsize=52,style=fruity" services/listen.py | pbcopy
```

# rebuild vagrant box

```shell
vagrant halt && vagrant destroy --force && vagrant up && vagrant ssh
```
