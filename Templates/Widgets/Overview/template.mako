<script id="Overview-template" type="text/x-handlebars-template">
<a class="named-anchor" name="overview"></a>
<div class="widget-grid-header"><i class="fas fa-tachometer-alt"></i>Overview</div>
<div class="widget-grid-item w4h1">
    <div class="widget-grid-item-inner">
        <table class="info-table">
            <tr>
                <th>Operating System</th>
                <td class="overview-platform">{{overview.osname}}</td>
            </tr>
            <tr>
                <th>Uptime</th>
                <td class="overview-uptime">{{overview.uptime}}</td>
            </tr>
            <tr>
                <th>Hostname</th>
                <td class="overview-hostname">{{overview,hostname}}</td>
            </tr>
            <tr>
                <th>IP Address</th>
                <td class="overview-ip">{{overview.primary_ip}}</td>
            </tr>
            <tr>
                <th>Kernel</th>
                <td class="overview-kernel">{{overview.kernel}}</td>
            </tr>
            <tr>
                <th>CPU(s)</th>
                <td class="overview-cpu">{{overview.cpus.cpus}} x {{overview.cpus.type}}</td>
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
