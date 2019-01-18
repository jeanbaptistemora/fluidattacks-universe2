sort ~/.ssh/known_hosts | uniq > ~/.ssh/known_hosts.uniq
mv -f ~/.ssh/known_hosts{.uniq,}
