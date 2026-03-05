# Coding Architecture II: FS26

## Week 03 - Reciprocal Frame Systems & Mesh Relaxation

![Course Banner](../../_static/caii-banner_fs26.jpg)

## Table of Contents

- [Introduction](#introduction)
- [VS Code Workflow](#vs-code-workflow)
- [Reciprocal Frame Systems](#reciprocal-frame-systems)
- [Iterative Algorithms](#iterative-algorithms)
- [Feedback Round](#feedback-round)
- [Design Session](#design-session)
- [Slides](#slides)
- [Examples](#examples)

## Introduction

In this week's lecture, we will cover the VS Code workflow, demonstrating how to edit files in VS Code and running the updated code directly in Rhino because of the use of the COMPAS auto-reloader. Then we will explore reciprocal frame systems in more depth, specifically focusing on the eccentricity of centerlines and how that part of the provided code works. We will also engage in a playful exploration of iterative algorithms, using mesh relaxation as an example. Finally, we will hold a feedback round and a dedicated design session for you to work on your initial sketch ideas for the project.

## VS Code Workflow

We will demonstrate how to efficiently work with files being edited in VS Code, while the auto-reloader allows you to run the updated code in Rhino. This continuous feedback loop is essential for rapidly testing and iterating on your geometric algorithms.

## Reciprocal Frame Systems

Continuing our exploration of Reciprocal Frame (RF) systems, we will dive into how the centerline eccentricity works. This will clarify how a part of the provided code functions and how it contributes to the overall behavior of the RF system. In an upcoming lecture, we will introduce additional mechanisms to the centerline eccentricity code.

## Iterative Algorithms

This part of the session is a playful exploration of how to write algorithms like mesh relaxation and similar iterative algorithms. We will learn how applying small, step-by-step updates can smoothly transform geometry into desired structural or aesthetic forms.

## Feedback Round

As usual, we will hold a short feedback and questions round in plenum using mentimeter.

## Design Session

You are encouraged to use this time to work on your initial sketch ideas for the project. Tutors will be available to discuss design logic, help translate ideas into computational workflows, and review your sketches.


## Slides

[![Slides](../../_static/slides.png)](https://docs.google.com/presentation/d/1DRe35_OqIhH_j6O-XMGzurAo3Ddp8OYEPFVxl3J4r-8)

<div style="display: flex; justify-content: center; align-items: center; height: 1vh;">
    <p style="font-size: 75%;">
        ↑ click to open ↑
    </p>
</div>

## Examples

The examples for this week can be found in the `lectures/week-03/examples` directory:

- [example-01-eccentricity.ghx](./examples/example-01-eccentricity.ghx)
- [example-02-relaxation.ghx](./examples/example-02-relaxation.ghx)
- [example-03-relax-visualization.ghx](./examples/example-03-relax-visualisation.ghx)