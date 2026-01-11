import React, { useRef, useEffect } from 'react';
import * as d3 from 'd3';

const GraphViewInteractive = ({ graphData }) => {
  const svgRef = useRef();
  const tooltipRef = useRef();

  useEffect(() => {
    if (!graphData) return;

    const width = 800;
    const height = 600;

    // Copias defensivas
    const nodes = graphData.nodes.map(n => ({ ...n }));
    const links = graphData.links.map(l => ({ ...l }));

    // Limpiar espacios en comunidades
    const cleanCommunities = nodes.map(n => n.community.trim());
    const communitySet = Array.from(new Set(cleanCommunities));
    const colorScale = d3.scaleOrdinal()
      .domain(communitySet)
      .range(d3.schemeCategory10);

    const svg = d3.select(svgRef.current);
    svg.selectAll('*').remove();

    const tooltip = d3.select(tooltipRef.current)
      .style('position', 'absolute')
      .style('pointer-events', 'none')
      .style('padding', '6px 10px')
      .style('background', 'rgba(0,0,0,0.7)')
      .style('color', '#fff')
      .style('border-radius', '4px')
      .style('font-size', '12px')
      .style('visibility', 'hidden');

    const container = svg.append('g');

    // Dibujar enlaces (sin posiciones iniciales)
    const linkElements = container.append('g')
      .attr('stroke', '#888')
      .attr('stroke-width', 1)
      .selectAll('line')
      .data(links)
      .join('line');

    // Dibujar nodos
    const nodeGroup = container.append('g');

    const circles = nodeGroup.selectAll('circle')
      .data(nodes)
      .join('circle')
      .attr('r', 8)
      .attr('fill', d => colorScale(d.community.trim()))
      .attr('stroke', '#333')
      .attr('stroke-width', 1)
      .style('cursor', 'pointer');

    // Tooltip
    circles
      .on('mouseover', (event, d) => {
        tooltip.style('visibility', 'visible')
          .html(`<strong>ID:</strong> ${d.id}<br/><strong>Community:</strong> ${d.community.trim()}`);
      })
      .on('mousemove', (event) => {
        tooltip.style('top', (event.pageY + 10) + 'px')
          .style('left', (event.pageX + 10) + 'px');
      })
      .on('mouseout', () => {
        tooltip.style('visibility', 'hidden');
      });

    // Zoom
    const zoom = d3.zoom()
      .scaleExtent([0.5, 5])
      .on('zoom', (event) => {
        const { transform } = event;
        container.attr('transform', `translate(${transform.x},${transform.y}) scale(${transform.k})`);
        circles.attr('r', 8 / transform.k);
        linkElements.attr('stroke-width', 1 / transform.k);
      });

    svg.call(zoom);

    // Simulación
    const simulation = d3.forceSimulation(nodes)
      .force('link', d3.forceLink(links).id(d => d.id).distance(50))
      .force('charge', d3.forceManyBody().strength(-120))
      .force('center', d3.forceCenter(width / 2, height / 2));

    simulation.on('tick', () => {
      linkElements
        .attr('x1', d => d.source.x)
        .attr('y1', d => d.source.y)
        .attr('x2', d => d.target.x)
        .attr('y2', d => d.target.y);

      circles
        .attr('cx', d => d.x)
        .attr('cy', d => d.y);
    });

    return () => simulation.stop(); // Limpieza
  }, [graphData]);

  return (
    <>
      <svg
        ref={svgRef}
        width="100%"
        height="600"
        style={{ border: '1px solid #ddd', backgroundColor: '#fff', cursor: 'grab' }}
        viewBox={`0 0 800 600`}
        preserveAspectRatio="xMidYMid meet"
      />
      <div ref={tooltipRef} />
    </>
  );
};

export default GraphViewInteractive;
