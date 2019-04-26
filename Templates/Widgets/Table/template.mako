<script id="Table-template" type="text/x-handlebars-template">
<div class="widget-grid-item {{widget.size}}">
    <div class="widget-grid-item-inner">
        <h1><i class="{{widget.fa_icon}}"></i>{{widget.title_label}}</h1>
        <table id="{{widget.id}}" class="data-table">
            <thead>
            <tr>
                {{#each widget.headers}}<th>{{this}}</th>{{/each}}
            </tr>
            </thead>
            <tbody>
            </tbody>
        </table>
    </div>
</div>
</script>
