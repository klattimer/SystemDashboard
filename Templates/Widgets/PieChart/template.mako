<script id="PieChart-template" type="text/x-handlebars-template">
<div class="widget-grid-item {{widget.size}}">
    <div class="widget-grid-item-inner">
        <div class="chart-container" id="{{widget.id}}-container">
            <canvas id="{{widget.id}}-chart-area"></canvas>
        </div>
        <div class="centre-label-large" id="{{widget.label_id}}">{{widget.label_value}}</div>
        <div class="centre-label-small">{{widget.label_small}}</div>
        <h1><i class="{{widget.fa_icon}}"/>{{widget.title_label}}</h1>
    </div>
</div>
</script>
