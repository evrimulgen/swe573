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
		"height": 500,
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
			.attr("dy", "1.7em")
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
			.style("fill", hexifyColor(pref.homefill));
 	
	left.selectAll("text")
 	     .data(data)
 	   .enter().append("text")
 	     .attr("x", function(d) {return partWidth - x(normNumeric(d.homeValue));})
 	     .attr("y", function(d) { return y(d.name) + y.rangeBand() / 2; })
 	     .attr("dx", 15) // padding-right
 	     .attr("dy", ".35em") // vertical-align: middle
 	     .attr("text-anchor", "start") // text-align: right
 		 .attr("class", "text label-text")
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
			.style("fill", hexifyColor(pref.awayfill));
			
	right.selectAll("text")
	     .data(data)
	   .enter().append("text")
	     .attr("x", function(d) {return x(normNumeric(d.awayValue));})
	     .attr("y", function(d) { return y(d.name) + y.rangeBand() / 2; })
	     .attr("dx", -15) // padding-right
	     .attr("dy", ".35em") // vertical-align: middle
	     .attr("text-anchor", "end") // text-align: right
		 .attr("class", "text label-text")
	     .text(function(d) {return beautifyText(d.awayValue);});
}
