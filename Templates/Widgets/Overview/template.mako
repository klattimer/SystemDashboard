<script id="Overview-template" type="text/x-handlebars-template">
<div class="widget-grid-item {{widget.size}}">
    <div class="widget-grid-item-inner">
        <table class="info-table">
            <tr>
                <th>Operating System</th>
                <td class="overview-platform"></td>
            </tr>
            <tr>
                <th>Uptime</th>
                <td class="overview-uptime"></td>
            </tr>
            <tr>
                <th>Hostname</th>
                <td class="overview-hostname"></td>
            </tr>
            <tr>
                <th>IP Address</th>
                <td class="overview-ip"></td>
            </tr>
            <tr>
                <th>Kernel</th>
                <td class="overview-kernel"></td>
            </tr>
            <tr>
                <th>CPU(s)</th>
                <td class="overview-cpu"></td>
            </tr>
        </table>
        <div id="overview-chart-area-container" class="chart-container noheader cw1h1"><canvas id="overview-chart-area"></canvas></div>
        <div id="stack">
            <div class="stack-item critical"><i class="fas fa-skull-crossbones"></i> 1 Critical</div>
            <div class="stack-item error"><i class="fas fa-exclamation-circle"></i> 1 Errors</div>
            <div class="stack-item warning"><i class="fas fa-exclamation-triangle"></i> 2 Warnings</div>
            <div class="stack-filler">Status OK</div>
        </div>
    </div>
</div>
</script>
