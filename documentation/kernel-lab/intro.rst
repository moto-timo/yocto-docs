.. SPDX-License-Identifier: CC-BY-SA-2.0-UK

************
Introduction
************

Welcome to the Yocto Project Hands-on Kernel Lab! During this session
you will learn how to work effectively with the Linux kernel within
the Yocto Project.
The 'Hands-on Kernel Lab' is actually a series of labs that will cover
the following topics:

  * Creating and using a traditional kernel recipe (":doc:`lab1`")
  * Using `bitbake -c menuconfig` to modify the kernel configuration
    and replace the defconfig with the new configuration
    (":doc:`lab1`")
  * Adding a kernel module to the kernel source and configuring it
    as a built-in module by adding options to the kernel defconfig
    (":doc:`lab1`")


  * Creating and using a linux-yocto-based kernel (":doc:`lab2`")
  * Adding a kernel module to the kernel source and configuring it
    as a built-in module using linux-yocto 'config fragments'
    (":doc:`lab2`")
  * Using the linux-yocto kernel as an LTSI kernel (configuring in an
    item added by the LTSI kernel which is merged into linux-yocto)
    (":doc:`lab2`")

  * Using an arbitrary git-based kernel via the linux-yocto-custom
    kernel recipe (":doc:`lab3`")
  * Adding a kernel module to the kernel source of an arbitrary
    git-based kernel and configuring it as a loadable module using
    'config fragments' (":doc:`lab3`")
  * Actually getting the module into the image and autoloading it on
    boot (":doc:`lab3`")


  * Using a local clone of an arbitrary git-based kernel via the
    linux-yocto-custom kernel recipe to demonstrate a typical
    development workflow (":doc:`lab4`")
  * Modifying the locally cloned custom kernel source and verifying
    the changes in the new image (":doc:`lab4`")
  * Using a local clone of a linux-yocto kernel recipe to demonstrate
    a typical development workflow (":doc:`lab4`")
  * Adding and using an external kernel module via a module recipe
    (":doc:`lab4`")

This lab assumes you have a basic understanding of the Yocto Project
and bitbake, and are comfortable navigating a UNIX filesystem from the
shell and issuing shell commands. If you need help in this area, please
consult the introductory material which you can find on the Yocto
website and/or Google for whatever else you need to know to get
started.

All of the material covered in this lab is documented in the
:doc:`/kernel-dev/index`.

Please consult the kernel development manual for more detailed
information and background on the topics covered in this lab.

.. tip::
   Throughout the lab you will need to edit various files. Sometimes
   the pathnames to these files are long. It is critical that you
   enter them exactly. Remember you can use the Tab key to help
   autocomplete path names from the shell. You may also copy and
   paste the paths from the PDF version of this lab which you can
   find at the same location that this document was found.

.. tip::
   Each lab is independent of the others and does not depend on the
   results of any previous lab, so feel free to jump right to any lab
   that is of interest to you.

Build System Basic Setup
========================

Preparing Your Build Environment
================================
