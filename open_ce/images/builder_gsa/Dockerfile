FROM centos:7
####################################################################################################
# gsa image
# Image to allow us to mount gsa using nfs. 
# 
# NOTES:
#
# - --cap-add sys_admin or privileged is needed to mount inside the docker image
# 
# - During run, the following commands need to be run to mount open-ce's gsa project space
#   echo <password> > gsa-login -c ausgsa <gsaid>
#   mount -o nolock ausgsa.ibm.com:/gsa/ausgsa/projects/o/open-ce/ /gsa/
####################################################################################################

ENV GSA_CLIENT=http://pokgsa.ibm.com/projects/g/gsa/client/linux/rhel7/gsa-client-3.0.15-17.el7.ppc64le.rpm
ENV CONDA_HOME=${CONDA_HOME:-/opt/conda}
ENV PATH=$CONDA_HOME/bin:$PATH
ENV CUDA_HOME=/usr/local/cuda

ENV OPEN_CE_CONDA_BUILD=3.20.5
RUN yum install -y ksh autofs nfs-utils bind-utils gcc make expect openldap-clients krb5-workstation perl

RUN curl -o gsa-client.rpm $GSA_CLIENT && rpm -ivh gsa-client.rpm && mkdir /gsa/

RUN export ARCH="$(uname -m)" && \
    curl -o /tmp/anaconda.sh https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-${ARCH}.sh && \
    chmod +x /tmp/anaconda.sh && \
    /bin/bash /tmp/anaconda.sh -f -b -p /opt/conda && \
    rm -f /tmp/anaconda.sh && \
    $CONDA_HOME/bin/conda install -y conda-build=${OPEN_CE_CONDA_BUILD}