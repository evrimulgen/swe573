/**
 Simple two-sided bar graph for Mac Merkezi Comparison Graph
 */

function simpleBar(divname, data, options){

    var	pref = {
        "awayfill": "F00",
        "homefill": "00F",
        "awaystroke": "F00",
        "homestroke": "00F",
        "width" : 800,
        "height": 400,
        "midmargin": 150
    }

    pref = $.extend(pref, options)

    //normalize numbers for better data visualization
    var normNumeric = function(x){
        return Math.log(x+1);
    }

    var hexifyColor = function(x){
        return "#" + x;
    }

    var beautifyText = function(x){
        if (x > 1000){
            return (x / 1000).toFixed(1) + " km";
        }
        else if (x < 2){
            return null;
        }
        else {
            return x;
        }
    }

    /* Declare margin, width, height params */
    var margin = {top: 20, right: 20, bottom: 30, left: 20}
        , width = pref.width - margin.left - margin.right
        , height = pref.height - margin.top - margin.bottom
        , midmargin = pref.midmargin;

    // the width of only one wing of the graph
    var partWidth = (width - midmargin)/2;

    var y = d3.scale.ordinal()
        .rangeRoundBands([0, height], .3);

    var x = d3.scale.linear()
        .range([0, partWidth]);

    var yAxis = d3.svg.axis()
        .scale(y)
        .orient("left");

    var svg = d3.select(divname).append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
        .append("g")
        .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

    y.domain(data.map(function(d) {
        return d.name;
    }));

    x.domain([0, d3.max(data, function(d) {
        return d3.max([normNumeric(d.homeValue), normNumeric(d.awayValue)]);
    })]);


    var left = svg.append("g")
        .attr("class", "leftwing")

    var mid = svg.append("g")
        .attr("class", "mid")
        .attr("transform", "translate(" + partWidth + ",0)")

    var right = svg.append("g")
        .attr("class", "rightwing")
        .attr("transform", "translate(" + (partWidth+midmargin) + ",0)" )

    mid.selectAll("text")
        .data(data)
        .enter().append("text")
        .attr("x", midmargin/2)
        .attr("y", function(d) {return y(d.name);})
        .attr("dx", 0)
        .attr("dy", "1.3em")
        .attr("text-anchor", "middle")
        .attr("class", "text mid-text")
        .text(function(d) {return d.name;});


    left.selectAll(".bar")
        .data(data)
        .enter().append("rect")
        .attr("class", "bar left")
        .attr("x", function(d) { return partWidth - x(normNumeric(d.homeValue)); })
        .attr("width", function(d) {return x(normNumeric(d.homeValue));})
        .attr("y", function(d) { return y(d.name); })
        .attr("rx", 6)
        .attr("ry", 6)
        .attr("height", function(d) { return y.rangeBand(); })
        .style("fill", hexifyColor(pref.homefill))
        .style("stroke-width", 3)
        .style("stroke", hexifyColor(pref.homestroke));

    left.selectAll("text")
        .data(data)
        .enter().append("text")
        .attr("x", function(d) {return partWidth - x(normNumeric(d.homeValue));})
        .attr("y", function(d) { return y(d.name) + y.rangeBand() / 2; })
        .attr("dx", 5) // padding-right
        .attr("dy", ".35em") // vertical-align: middle
        .attr("text-anchor", "start") // text-align: right
        .attr("class", "text label-text")
        .style("color",hexifyColor(pref.homestroke))
        .style("fill", hexifyColor(pref.homestroke))
        .text(function(d) {return beautifyText(d.homeValue);});

    right.selectAll(".bar")
        .data(data)
        .enter().append("rect")
        .attr("class", "bar right")
        .attr("x", function(d) { return 0; })
        .attr("width", function(d) {return x(normNumeric(d.awayValue));})
        .attr("y", function(d) { return y(d.name); })
        .attr("rx", 6)
        .attr("ry", 6)
        .attr("height", function(d) { return y.rangeBand(); })
        .style("fill", hexifyColor(pref.awayfill))
        .style("stroke-width", 3)
        .style("stroke", hexifyColor(pref.awaystroke));

    right.selectAll("text")
        .data(data)
        .enter().append("text")
        .attr("x", function(d) {return x(normNumeric(d.awayValue));})
        .attr("y", function(d) { return y(d.name) + y.rangeBand() / 2; })
        .attr("dx", -5) // padding-right
        .attr("dy", ".35em") // vertical-align: middle
        .attr("text-anchor", "end") // text-align: right
        .attr("class", "text label-text")
        .style("color",hexifyColor(pref.awaystroke))
        .style("fill", hexifyColor(pref.awaystroke))
        .text(function(d) {return beautifyText(d.awayValue);});
}

/*
 Alternating Bar Chart for Player/Team Stats
 */

// Source : http://mbostock.github.io/d3/tutorial/bar-1.html


function feedWithRandomData()
{

    var dataset = [],
        i = 0;

    for(i=0; i<15; i++){
        dataset.push(Math.round(Math.random()*100));
    }
    objectChart.updateChart(dataset);
}


function d3BarChart(){

    var chartXCoefficient;
    var chartYCoefficient;
    var elementToDraw = "body";;
    var chartHeight = 200;
    var chartWidth = 500;
    var tooltip;
    var fontFamily = "Verdana";
    var chartTextSize = 10;
    var dataset = [45, 48, 42, 36, 35, 31, 38, 39, 12,100,36,42];
    var textSizeCoefficient = 1.3;
    var hoverColor = "red";

    this.drawChart =  function (elementID,width, height, data)
    {

        if(width != null)
        {
            chartWidth = width;
        }

        if(height != null )
        {
            chartHeight = height;
        }

        if(data != null )
        {
            dataset = data;


            while(dataset.length < 15)
            {
                dataset.push(0);
            }
        }

        if(elementID != null)
        {
            elementToDraw = "#" + elementID;
        }

        chartWidth = chartWidth -chartTextSize;

        chartXCoefficient = chartWidth / 15;
        chartYCoefficient = chartHeight / (d3.max(dataset)*1.3);

        var chartXCoefficient2  = d3.scale.linear()
            .domain([0, d3.max(dataset)*1.3])
            .range([0, chartHeight- chartTextSize]);

        var chartYCoefficient2  = d3.scale.ordinal()
            .domain(dataset)
            .rangeBands([0, chartHeight]);

        tooltip = d3.select(elementToDraw)
            .append("div")//.attr("class","toolTip")
            .style("font-size",(chartTextSize + "px"))
            .style("position", "absolute")
            .style("z-index", "10")
            .style("visibility", "hidden")
            .style("font-family",fontFamily)
            .text("a simple tooltip");

        var chart = d3.select(elementToDraw).append("svg")
            .attr("class", "chart")
            .attr("width", chartWidth)
            .attr("height",chartHeight);

        chartHeight = chartHeight - chartTextSize;

        var ticks = chartXCoefficient2.ticks(10);
        ticks[ticks.length] = 0;

        chart.selectAll("line")
            .data(chartXCoefficient2.ticks(10))
            .enter().append("line")
            .attr("x1", 0)
            .attr("x2", chartWidth)
            .attr("y1", chartXCoefficient2)
            .attr("y2", chartXCoefficient2)
            .style("stroke", "#ccc");

        chart.selectAll("rect")
            .data(dataset)
            .enter().append("rect")
            .attr("y", function(d,i) {return chartHeight - d*chartYCoefficient})
            .attr("x", function(d,i) {return i*chartXCoefficient})
            .attr("width", chartXCoefficient)
            .attr("height", function(d,i) {return d*chartYCoefficient})
            .on("mouseover", function(d,i){

                console.log(d3.select(this).attr("x"));
                console.log(chartXCoefficient);

                var xValue = parseInt(d3.select(this).attr("x"),10) ;
                xValue += chartXCoefficient / 2;
                var yValue = parseInt(d3.select(this).attr("y"), 10);


                if(yValue < 0)
                    yValue += 23;
                else
                    yValue += 10;

                if(yValue + 10  > chartHeight)
                {
                    yValue -= 20;

                }

                console.log(xValue);
                d3.select(this).style("fill",hoverColor);
                tooltip.style("top",
                    yValue+"px").style("left",xValue+"px");
                tooltip.text(d);
                return tooltip.style("visibility", "visible");

            })
            .on("mouseout", function(){
                d3.select(this).style("fill","darkred")
                return tooltip.style("visibility", "hidden");});

        chart.selectAll("text")
            .data(dataset)
            .enter().append("text")
            //.attr("font-size","15px")
            .style("font-family",fontFamily)
            .attr("font-size",chartTextSize)
            .attr("x", function(d,i) {return i*chartXCoefficient + chartXCoefficient / 2})
            .attr("y", function(d,i) {return chartHeight + chartTextSize})
            .attr("dx", chartTextSize/3) // padding-right
            //.attr("dy", ".35em") // vertical-align: middle
            .attr("text-anchor", "end") // text-align: right
            .text(function(d,i) {return i + 1});

        chart.selectAll("text")
            .data(dataset)
            .enter().append("text")
            .style("font-family", fontFamily)
            .attr("font-size", chartTextSize)
            .attr("x", function(d,i) {return (i+0.5)*chartXCoefficient;})
            .attr("text-anchor", "middle")
            //.attr("y", )

    }


    this.updateChart = function  (datasetNew)
    {
        while( datasetNew.length < 15)
        {
            datasetNew.push(0);
            console.log(dataset);
        }

        chartXCoefficient = chartWidth / datasetNew.length;
        chartYCoefficient = chartHeight / (d3.max(datasetNew)*1.3);

        var chart = d3.select(elementToDraw).selectAll("rect").data(datasetNew);

        //chart.selectAll("rect")
        chart
            .on("mouseover", function(d,i){
                d3.select(this).style("fill",hoverColor);

                var xValue = parseInt(d3.select(this).attr("x"),10) ;
                xValue += chartXCoefficient / 2;
                var yValue = parseInt(d3.select(this).attr("y"), 10);


                if(yValue < 0)
                    yValue += 23;
                else
                    yValue += 10;


                if(yValue + chartTextSize > chartHeight)
                {
                    yValue -= 20;

                }

                tooltip.style("top",
                    //(d3.event.pageY-10)+"px").style("left",(d3.event.pageX+10)+"px");
                    yValue+"px").style("left",xValue+"px");
                tooltip.text(d);
                return tooltip.style("visibility", "visible");
            })
            .transition()
            .duration(1000)
            .attr("y", function(d,i) {return chartHeight - d*chartYCoefficient})
            .attr("x", function(d,i) {return i*chartXCoefficient})
            .attr("width", chartXCoefficient)
            .attr("height", function(d,i) {return d*chartYCoefficient});


        chart.exit().transition()
            .duration(1000)
            .attr("height", 0)
            .remove();


        chart = d3.select(elementToDraw).selectAll("text").data(datasetNew);


        chart.enter().append("text")
            .style("font-family",fontFamily)
            .attr("font-size",chartTextSize)
            .attr("x", function(d,i) {return i*chartXCoefficient + chartXCoefficient / 2})
            .attr("y", function(d,i) {return chartHeight + chartTextSize})
            .attr("dx", chartTextSize/3)
            .attr("text-anchor", "end")
            .text(function(d,i) {return i + 1});

        chart.exit().transition()
            .duration(1000)
            .attr("height", 0)
            .remove();

        var lineScale  = d3.scale.linear()
            .domain([0, d3.max(dataset)])
            .range([0, chartWidth]);

        chart = d3.select(elementToDraw).selectAll("line").data(lineScale.ticks(10))
            .enter().append("line")
            .attr("x1", 0)
            .attr("x2", chartWidth)
            .attr("y1", lineScale)
            .attr("y2", lineScale)
            .style("stroke", "#ccc");

        chart.transition()
            .duration(1000)
            .attr("width", 0)
            .remove();
    }
}


function drawLineChart(elementID, dataArray, options)
{
    var fontFamily = "sans-serif";
    var chartTextSize = 9;
    var nodeRadius = 6;

    //Argument controls
    if(elementID == null)
    {
        return "Error : elementID is null";
    }
    if(dataArray == null)
    {
        //To draw something  with default dataset
        dataArray = [5,6,3,8,6,9,10,5,7,3,2,1,10,3];
        console.log("Data Array was selected as default data array..");
    }

    var m = [5, 10, 20, 10]; // margins
    var w = options.width - m[1] - m[3]; // width
    var h = 300 - m[0] - m[2]; // height

    // create a simple data array that we'll plot with a line (this array represents only the Y values, X will just be the index location)
    var data = dataArray;

    // X scale will fit all values from data[] within pixels 0-w
    var x = d3.scale.linear().domain([1, 34]).range([0, w]);
    // Y scale will fit values from 0-10 within pixels h-0 (Note the inverted domain for the y-scale: bigger is up!)
    var y = d3.scale.linear().domain([18,0]).range([h - 7, 0]);
    // automatically determining max range can work something like this
    // var y = d3.scale.linear().domain([0, d3.max(data)]).range([h, 0]);

    // create a line function that can convert data[] into x and y points
    var line = d3.svg.line()
        // assign the X function to plot our line as we wish
        .x(function(d,i) {
            return x(i+1);
        })
        .y(function(d) {
            return y(d);
        })

    var graph = d3.select("#" + elementID).append("svg:svg")
        .attr("width", w + m[1] + m[3])
        .attr("height", h + m[0] + m[2])
        .append("svg:g")
        .attr("transform", "translate(" + m[3] + "," + m[0] + ")");

    var xAxis = d3.svg.axis().scale(x).ticks(34).tickSize(-h).tickSubdivide(true);

    graph.append("svg:g")
        .attr("class", "x axis")
        .attr("transform", "translate(0," + h + ")")
        .call(xAxis);

    graph.append("svg:path").attr("d", line(data));

    var group = graph.selectAll("g.nodess").data(data).enter().append("g").attr("class","nodess")

    group
        .append("circle")
        .attr("fill","white")
        .attr("stroke","darkred")
        .attr("stroke-width",1)
        .attr("r", nodeRadius)
        .attr("cx",function(d,i) { return x(i) + 5 + nodeRadius + nodeRadius / 2; })
        .attr("cy", function(d,i) { return y(d) ; });

    group
        .append("text")
        .style("font-family",fontFamily)
        .attr("font-size",chartTextSize)
        .attr("cursor","default")
        .attr("font-weight","bold")
        .attr("x", function(d,i) { if(d > 9) return x(i) + 9.5 ; return x(i) + 8; })
        .attr("y", function(d,i) {  return y(d) + 3 ; })
        .attr("dx", chartTextSize) // padding-right
        .attr("text-anchor", "end") // text-align: right
        .text(function(d,i) {  return d});


    graph.append("text")
        .attr("text-anchor", "end")
        .attr("font-size", 10)
        .attr("font-family", "sans-serif")
        .attr("x",m[2])
        .attr("y",295)
        .text("Hafta");

}

/*
    Comparison Type bar chart for the Comparison view
    An implementation of simple bar
 */

function comparisonBar() {

    this.draw = function(divname, data, options){

        var	pref = {
            "awayfill": "F00",
            "homefill": "00F",
            "awaystroke": "F00",
            "homestroke": "00F",
            "width" : 800,
            "height": 400,
            "midmargin": 150
        }

        pref = $.extend(pref, options)

        //normalize numbers for better data visualization
        var normNumeric = function(x){
            return Math.log(x+1);
        }

        var hexifyColor = function(x){
            return "#" + x;
        }

        var beautifyText = function(x){
            if (x > 1000){
                return (x / 1000).toFixed(1) + " km";
            }
            else if (x < 2){
                return null;
            }
            else {
                return x;
            }
        }

        /* Declare margin, width, height params */
        var margin = {top: 20, right: 20, bottom: 30, left: 20}
            , width = pref.width - margin.left - margin.right
            , height = pref.height - margin.top - margin.bottom
            , midmargin = pref.midmargin;

        // the width of only one wing of the graph
        var partWidth = (width - midmargin)/2;

        var y = d3.scale.ordinal()
            .rangeRoundBands([0, height], .3);

        var x = d3.scale.linear()
            .range([0, partWidth]);

        var yAxis = d3.svg.axis()
            .scale(y)
            .orient("left");

        var svg = d3.select(divname).append("svg")
            .attr("width", width + margin.left + margin.right)
            .attr("height", height + margin.top + margin.bottom)
            .append("g")
            .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

        y.domain(data.map(function(d) {
            return d.name;
        }));

        x.domain([0, d3.max(data, function(d) {
            return d3.max([normNumeric(d.homeValue), normNumeric(d.awayValue)]);
        })]);


        var left = svg.append("g")
            .attr("class", "leftwing")

        var mid = svg.append("g")
            .attr("class", "mid")
            .attr("transform", "translate(" + partWidth + ",0)")

        var right = svg.append("g")
            .attr("class", "rightwing")
            .attr("transform", "translate(" + (partWidth+midmargin) + ",0)" )

        mid.selectAll("text")
            .data(data)
            .enter().append("text")
            .attr("x", midmargin/2)
            .attr("y", function(d) {return y(d.name);})
            .attr("dx", 0)
            .attr("dy", "1.3em")
            .attr("text-anchor", "middle")
            .attr("class", "text mid-text")
            .text(function(d) {return d.name;});


        left.selectAll(".bar")
            .data(data)
            .enter().append("rect")
            .attr("class", "bar left")
            .attr("x", function(d) { return partWidth - x(normNumeric(d.homeValue)); })
            .attr("width", function(d) {return x(normNumeric(d.homeValue));})
            .attr("y", function(d) { return y(d.name); })
            .attr("rx", 6)
            .attr("ry", 6)
            .attr("height", function(d) { return y.rangeBand(); })
            .style("fill", hexifyColor(pref.homefill))
            .style("stroke-width", 3)
            .style("stroke", hexifyColor(pref.homestroke));

        left.selectAll("text")
            .data(data)
            .enter().append("text")
            .attr("x", function(d) {return partWidth - x(normNumeric(d.homeValue));})
            .attr("y", function(d) { return y(d.name) + y.rangeBand() / 2; })
            .attr("dx", 5) // padding-right
            .attr("dy", ".35em") // vertical-align: middle
            .attr("text-anchor", "start") // text-align: right
            .attr("class", "text label-text")
            .style("color",hexifyColor(pref.homestroke))
            .style("fill", hexifyColor(pref.homestroke))
            .text(function(d) {return beautifyText(d.homeValue);});

        right.selectAll(".bar")
            .data(data)
            .enter().append("rect")
            .attr("class", "bar right")
            .attr("x", function(d) { return 0; })
            .attr("width", function(d) {return x(normNumeric(d.awayValue));})
            .attr("y", function(d) { return y(d.name); })
            .attr("rx", 6)
            .attr("ry", 6)
            .attr("height", function(d) { return y.rangeBand(); })
            .style("fill", hexifyColor(pref.awayfill))
            .style("stroke-width", 3)
            .style("stroke", hexifyColor(pref.awaystroke));

        right.selectAll("text")
            .data(data)
            .enter().append("text")
            .attr("x", function(d) {return x(normNumeric(d.awayValue));})
            .attr("y", function(d) { return y(d.name) + y.rangeBand() / 2; })
            .attr("dx", -5) // padding-right
            .attr("dy", ".35em") // vertical-align: middle
            .attr("text-anchor", "end") // text-align: right
            .attr("class", "text label-text")
            .style("color",hexifyColor(pref.awaystroke))
            .style("fill", hexifyColor(pref.awaystroke))
            .text(function(d) {return beautifyText(d.awayValue);});
    }
}
