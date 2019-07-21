<script id="Table-template" type="text/x-handlebars-template">
<div id="{{widget.id}}" class="widget-grid-item {{widget.size}}">
    <div class="widget-grid-item-inner">
        <h1><i class="{{widget.fa_icon}}"></i>{{widget.title_label}}</h1>
        <table class="data-table">
            <thead>
            <tr>
                {{#each widget.headers}}<th class="{{this.class}}">{{this.title}}</th>{{/each}}
            </tr>
            </thead>
            <tbody>
            </tbody>
        </table>
    </div>
</div>
</script>
