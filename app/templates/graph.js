<script type="text/javascript">
    function get2dContext(id){
        return document.getElementById(id).getContext("2d");
    }

    function drawPieChart(context, data, options){
        new Chart(context).Pie(data, options)
    }
  
    var data = [
    {
        value: {{failed}},
        color:"#F7464A",
        highlight: "#FF5A5E",
        label: "Failed"
    },
    {
        value: {{passed}},
        color: "#19A347",
        highlight: "#4DB870",
        label: "Passed"
    },
]

    $(document).ready(function() {
        var ctx = get2dContext('graph'); 
        
        drawPieChart(ctx, data, {});
        $("#dt").dataTable({
            "lengthMenu": [[5, 15, 25, -1], [5, 15, 25, "All"]],
            "order": [[3, "desc"]]
        });
    }); 
</script>
