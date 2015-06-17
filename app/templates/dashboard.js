<script type="text/javascript">
    function get2dContext(id){
        return document.getElementById(id).getContext("2d");
    }

    function drawLineChart(context, data, options){
        return new Chart(context).Line(data, options);
    }
    
    function drawBarChart(context, data, options){
        return new Chart(context).Bar(data, options);
    }

    var labels = [ 
        {% for b in build %}
        '{{b.name}}',
        {% endfor %}
    ]
            
            var opt1 = {
        animation: false,
        scaleLabel : "<%= value +' K'%>"
    };

            var opt2 = {
        animation: false,
        scaleLabel : "<%= value +' G'%>"
    };

    var cpsData = {
        labels: labels, 
           datasets: [
            {
                label: "My First dataset",
                fillColor: "rgb(128, 204, 204)",
                strokeColor: "rgb(128, 204, 204)",
                pointColor: "rgb(128, 204, 204)",
                pointStrokeColor: "#fff",
                pointHighlightFill: "#fff",
                pointHighlightStroke: "rgba(220,220,220,1)",
                
                data: [ {% for cps_data in cps %}{{cps_data.cps}},{% endfor %}]
            },

        ]
    };

    var hpsData = {
        labels: labels,

        datasets: [
            {
                label: "My First dataset",
                fillColor: "rgb(128, 204, 153)",
                strokeColor: "rgb(128, 204, 153)",
                pointColor: "rgb(128, 204, 153)",
                pointStrokeColor: "#fff",
                pointHighlightFill: "#fff",
                pointHighlightStroke: "rgba(220,220,220,1)",
                data: [ {% for hps_data in hps %}{{hps_data.hps/10}},{% endfor %}]
            },

        ]
    };
    var throughputData = {
        labels: labels, 
        datasets: [
            {
                label: "My First dataset",
                fillColor: "rgb(112, 148, 219)",
                strokeColor: "rgb(112, 148, 219)",
                pointColor: "rgb(112, 148, 219)",
                pointStrokeColor: "#fff",
                pointHighlightFill: "#fff",
                pointHighlightStroke: "rgba(220,220,220,1)",
                data: [ {% for tdata in throughput %}{{tdata.throughput/100}},{% endfor %}]
            },
        ]
    };
    smokelabels = [{% for build in smoke_results %}"{{build.name}}",{% endfor %}];
    var smokeData = {
            labels: smokelabels, 
            datasets: [
                {
                    label: "Failed",
                    fillColor: "rgb(255, 102, 102)",
                    strokeColor: "rgb(255, 102, 102)",
                    highlightFill: "rgb(255, 102, 102)",
                    highlightStroke: "rgb(255, 102, 102)",
                    data: [{% for smoke in smoke_results %}{{smoke.failed}},{% endfor %}]
                },
                {
                    label: "Passed",
                    fillColor: "rgb(128, 204, 153)",
                    strokeColor: "rgb(128, 204, 153)",
                    highlightFill: "rgb(128, 204, 153)",
                    highlightStroke: "rgb(128, 204, 153)",
                    data: [{% for smoke in smoke_results %}{{smoke.passed}},{% endfor %}]
                },
                {
                    label: "Total",
                    fillColor: "rgb(133, 163, 194)",
                    strokeColor: "rgb(133, 163, 194)",
                    highlightFill: "rgb(133, 163, 194)",
                    highlightStroke: "rgb(133, 163, 194)",
                    data: [{% for smoke in smoke_results %}{{smoke.total}},{% endfor %}]
                },
            ]
        };

    reglabels = [{% for build in reg_results %}"{{build.name}}",{% endfor %}];
    var regData = {
            labels: reglabels, 
            datasets: [
                {
                    label: "Failed",
                    fillColor: "rgb(255, 102, 102)",
                    strokeColor: "rgb(255, 102, 102)",
                    highlightFill: "rgb(255, 102, 102)",
                    highlightStroke: "rgb(255, 102, 102)",
                    data: [{% for reg in reg_results %}{{reg.failed}},{% endfor %}]
                },
                {
                    label: "Passed",
                    fillColor: "rgb(128, 204, 153)",
                    strokeColor: "rgb(128, 204, 153)",
                    highlightFill: "rgb(128, 204, 153)",
                    highlightStroke: "rgb(128, 204, 153)",
                    data: [{% for reg in reg_results %}{{reg.passed}},{% endfor %}]
                },
                {
                    label: "Total",
                    fillColor: "rgb(133, 163, 194)",
                    strokeColor: "rgb(133, 163, 194)",
                    highlightFill: "rgb(133, 163, 194)",
                    highlightStroke: "rgb(133, 163, 194)",
                    data: [{% for reg in reg_results %}{{reg.total}},{% endfor %}]
                },
            ]
        };


    $(document).ready(function() {
        var cpsContext = get2dContext('cps'); 
        var hpsContext = get2dContext('hps'); 
        var throughputContext = get2dContext('throughput'); 
        var smokeContext = get2dContext('smoke'); 
        var regressionContext = get2dContext('regression');
        
        drawLineChart(cpsContext ,cpsData, {}); 
        drawLineChart(hpsContext, hpsData, opt1); 
        drawLineChart(throughputContext, throughputData, opt2); 
        drawBarChart(smokeContext, smokeData, {}); 
        drawBarChart(regressionContext, regData, {});
    }); 
</script>
