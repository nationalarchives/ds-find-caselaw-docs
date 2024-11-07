# 21. Standardising our colour variable naming convention

Date: 2024-11-07

## Status

Proposed

## Context

### Background

We currently lack a consistent colour variable naming convention. This has led to several issues:

 - The same colour value has been defined as multiple different variables with different names
 - Similar but distinct colour values have been defined without consideration to the existing variables, resulting in redundant variables
 - Colours are sometimes added to codebases without being assigned a variable for reuse
 - As a result of there being limited design oversight for a time, there are multiple colours that have been defined without knowledge of where they were used or how they are expected to be used
 - Colours have been imported from external sources without being added to the central colour variable list

Currently, colours are either defined by their visual colour, e.g. `$color-yellow`, or for the context in which they were first used, e.g. `$color-linked-disabled**

### Problem

The lack of a naming convention for colours has resulted in:

 - Reduced reusability and maintainability of colour variables
 - Difficulty in tracking colour usage across components
 - Fragmented design that can lead to an inconsistent user experience
 - Increased development effort due to redundant variables and difficulty updating colours across the codebase

### Goals

This ADR proposed a naming convention that:

 - Promotes reuse of colour variables
 - Improves consistency across the codebase
 - Aligns with industry standards

### Options considered

**Material UI**

 - **Naming convention:** Organised by name and shade via brackets (like you are accessing a value in a map via a key), e.g. `blue[50]`, `blue[500]`
 - **Pros:**
	 - Clear hierarchical naming structure
	 - Shades are organised by a numeric scale, making it easy to adjust lightness/darkness
 - **Cons:**
	 - Bracket notation, i.e. `colour[50]`, hides complexity of what a colour value actually is
	 - Doesn't necessarily indicate how a colour should be used

**Tailwind CSS**

 - **Naming convention:** Organised by name and shade with statically defined variables, i.e. `blue-50`, `blue-500`
 - **Pros:**
	 - Clear hierarchical naming structure
	 - Shades are organised by a numeric scale making it easy to choose the appropriate lightness/darkness
	 - Easily maintainable/ease to add new colours
 - **Cons:**
	 - Fixed naming means if similar shades of colours are added, variables may need to be adjusted to accomodate
	 - Doesn't necessarily indicate how a colour should be used

**Bootstrap**

 - **Naming convention:** They use a set of semantic names, e.g. `primary`, `secondary`, `success`
 - **Pros:**
	 - Simple set of semantic colours indicate where a colour should be used
 - **Cons:**
	 - Limits flexibility where a semantic name is used in a place that doesn't make sense
	 - Requires duplication of colour values where similar values are used for different purposes

**Ant Design**

 - **Naming convention:** Organised by semantic colour name and shade, e.g. `primary-1`, `secondary-5`
 - **Props:**
	 - Semantic colours indicate where a colour should be used
	 - Numbering system gives flexibility on tones
 - **Cons:**
	 - Limits flexibility where a semantic name is used in a place that doesn't make sense
	 - With the number of potential variants on a single colour, it doesn't really give you the value of having semantic colours indicating usage anymore

**Chakra UI**

- **Naming convention:** Organised by name and shade, split by a period, i.e. `blue.50`, `blue.500`
- **Props:**
	- Clear hierarchical naming structure
	- Shades are organised by a numeric scale making it easy to choose the appropriate lightness/darkness
	- Easily maintainable/ease to add new colours
- **Cons:**
	- Fixed naming means if similar shades of colours are added, variables may need to be adjusted to accomodate
	- Doesn't necessarily indicate how a colour should be used

## Decision

### Proposed solution

Adopt a solution most similar to Tailwind naming convention for colour variables, using the format `$color-colorName-shade`, e.g. `$color-blue-50`, `$color-blue-500`.

### Justification

This naming convention was chosen due the following:

- Clear hierarchical naming structure
- Easy to maintain and add new colours to
- Aligns with industry standards
- All our other variables use a hyphen to split the various parts of the variable
- To help with readability, we will prepend the word `color` to the variables to be explicit the variable is a colour

## Consequences

- Increased maintainability of colour variables
- Consistency and readability of code, allowing developers to quickly identify colours
- Consistency for users, with a standard colour scheme being used throughout the app
- Single colour language means quick and easy handoff from design to development - can refer to existing colour names instead of hex codes
