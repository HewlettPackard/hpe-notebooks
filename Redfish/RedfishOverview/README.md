# Welcome to the Redfish Overview HPE Notebook

Version 0.45

Companion Redfish articles on the [HPE Developer site](https://developer.hpe.com/blog)

## Introduction to the Redfish API With PowerShell Python and Bash/cURL

The goal of these Jupyter Notebooks is to learn the basics of the Redfish standard REST API. After a quick positioning of this API, you'll explore a Redfish tree to understand its basic structure. In addition we'll learn how to modify resources and perform actions using different tools. Best practices will be presented as well. Beginners and experts are welcome.

<img src="https://redfish.dmtf.org/sites/default/files/DMTF_Redfish_logo_R.jpg" alt="Redfish Logo" style="width: 125px;"/> 

### What is Redfish

As per the [Redfish](https://www.dmtf.org/standards/redfish) home page, DMTF Redfish® is a standard designed to deliver **simple and secure management** for converged, hybrid IT and the Software Defined Data Center (SDDC)".

### Workshop goal

At the end of the workshop, you should be able to 1) explain the basic architecture of the Redfish resource tree; 2) explain why it is crucial to follow [best practices](https://developer.hpe.com/blog/getting-started-with-ilo-restful-api-redfish-api-conformance) when programming the Redfish API; and 3) explain the session-based authentication mechanism.

### Workshop infrastructure

Each student, or team, has a dedicated [Jupyter](https://jupyter.org/) environment hosted by a Linux host that provides a set of [Jupyter notebooks](https://jupyter-notebook-beginner-guide.readthedocs.io/en/latest/what_is_jupyter.html).

The notebooks can access a dedicated [OpenBMC](https://www.openbmc.org/) appliance simulator with `GET` and `SET` methods, and a shared [HPE iLO 5](http://hpe.com/info/ilo) (in `GET` mode only).

![ProgrammingRedfsihInfrastructureDescription](Pictures/ProgrammingRedfishInfraDescription.png)

## Lab description

> **NOTE**: Since the content of [Lab 1](1-RedfishBash.ipynb) and [Lab 2](2-RedfishPowerShell.ipynb) are identical, you can choose either one depending on your skills and preferences. If you are more Linux/Bash/cURL oriented, choose  [Lab 1](1-RedfishBash.ipynb). If you are more Windows/PowerShell focused, choose [Lab 2](2-RedfishPowerShell.ipynb). 

### [Lab 1](1-RedfishBash.ipynb): Redfish overview using Bash/cURL

Redfish tree overview using [Bash](https://www.gnu.org/software/bash/) and [cURL](https://curl.haxx.se/) tool against an OpenBMC simulator followed by a reset of the OpenBMC. Choose this lab if you are more Linux/Bash/cURL oriented.

### [Lab 2](2-RedfishPowerShell.ipynb): Redfish overview using PowerShell

Identical to Lab 1, but uses PowerShell commands. Choose this lab if you are more Windows/PowerShell focused.

### [Lab 3](3-RedfishPython.ipynb): Browsing multiple Redfish implementations using a single piece of code

Single Python program to retrieve MAC addresses from an OpenBMC and from an HPE iLO 5.
