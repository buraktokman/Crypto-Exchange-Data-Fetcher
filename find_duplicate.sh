# Ask question if awk found a duplicate

awk 'a[$0]++{exit 1}' $1 || (
    echo -n "remove duplicates? [y/n] "
    read answer
    # Remove duplicates if answer was "y" . I'm using `[` the shorthand
    # of the test command. Check `help [`
    [ "$answer" == "y" ] && uniq $1 > $1.no-duplicate
)