function bondedCatsComponent(catId, initialSelected) {
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
            // Prevent selecting the cat itself
            if (cat.id === catId) {
                return;
            }

            this.selected.push(cat);
            this.selectedIds.push(cat.id);
            this.results = [];
            this.query = "";
        },

        remove(id) {
            this.selected = this.selected.filter(c => c.id !== id);
            this.selectedIds = this.selectedIds.filter(x => x !== id);
        }
    }
}
