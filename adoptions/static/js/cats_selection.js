function catsSelectionComponent(initialSelected) {
    return {
        query: "",
        results: [],
        selected: [],
        selectedIds: [],

        init() {
            if (initialSelected.length > 0) {
                fetch(`/cats/get-by-ids/?` + new URLSearchParams(initialSelected.map(id => ['ids[]', id])))
                    .then(r => r.json())
                    .then(data => {
                        this.selected = data;
                        this.selectedIds = initialSelected;
                    });
            }
        },

        search() {
            if (this.query.length < 2) {
                this.results = [];
                return;
            }

            fetch(`/cats/search/?q=${this.query}`)
                .then(r => r.json())
                .then(data => {
                    // Exclude already selected
                    this.results = data.filter(c => !this.selectedIds.includes(c.id));
                });
        },

        add(cat) {
            this.selected.push(cat);
            this.selectedIds.push(cat.id);

            // If this cat has bonded cats, add them too
            if (cat.bonded_cats && cat.bonded_cats.length > 0) {
                cat.bonded_cats.forEach(bondedCatId => {
                    if (!this.selectedIds.includes(bondedCatId)) {
                        // Fetch the bonded cat details
                        fetch(`/cats/get-by-ids/?ids[]=${bondedCatId}`)
                            .then(r => r.json())
                            .then(data => {
                                if (data.length > 0) {
                                    this.selected.push(data[0]);
                                    this.selectedIds.push(bondedCatId);
                                }
                            });
                    }
                });
            }

            this.results = [];
            this.query = "";
        },
        // Compute connected groups among selected cats using their bonded links
        groups() {
            const map = new Map(this.selected.map(c => [c.id, c]));
            const visited = new Set();
            const groups = [];

            for (const cat of this.selected) {
                if (visited.has(cat.id)) continue;
                const stack = [cat.id];
                const comp = [];

                while (stack.length) {
                    const id = stack.pop();
                    if (visited.has(id)) continue;
                    visited.add(id);
                    const node = map.get(id);
                    if (node) comp.push(node);

                    const neighbours = (node && node.bonded_cats) ? node.bonded_cats : [];
                    neighbours.forEach(nid => {
                        if (this.selectedIds.includes(nid) && !visited.has(nid)) stack.push(nid);
                    });
                }

                groups.push(comp);
            }

            return groups;
        },

        removeGroup(ids) {
            this.selected = this.selected.filter(c => !ids.includes(c.id));
            this.selectedIds = this.selectedIds.filter(x => !ids.includes(x));
        },

        remove(id) {
            // Find the group containing this id and remove the whole group
            const grp = this.groups().find(g => g.some(c => c.id === id));
            if (grp) {
                this.removeGroup(grp.map(c => c.id));
            } else {
                this.removeGroup([id]);
            }
        }
    }
}
