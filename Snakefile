
UNIPROT_ID = config['id']

rule all:
    input:
        results = 'cool_results'


rule download_databases:
    output:
        uniprot = temp("databases/uniprot.txt"),
        scop = temp("databases/scop.txt")
    log:
        "logs/download_databases.log"
    threads:
        workflow.cores
    message:
        "Downloading Uniprot and SCOP Databases..."
    shell:
        """
        wget https://scop.mrc-lmb.cam.ac.uk/files/scop-cla-latest.txt -O databases/scop.txt |& tee -a {log}
        wget https://ftp.uniprot.org/pub/databases/uniprot/current_release/knowledgebase/complete/docs/similar.txt -O databases/uniprot.txt |& tee -a {log}
        """

rule get_domains:
    input:
        uniprot = "databases/uniprot.txt",
        scop = "databases/scop.txt"
    output:
        summary = "text/summary.txt"
    log:
        "logs/get_domains.log"
    threads:
        workflow.cores
    message:
        "Finding domains and defining protein family..."
    shell:
        """
        mkdir -p text
        sed '/{UNIPROT_ID}/q' databases/uniprot.txt | grep family \
        | tail -1 | sed -e '1 i Protein Family:' > text/summary.txt |& tee -a {log}
        
        cat scop-cla-latest.txt | grep {UNIPROT_ID} \
        | awk '{{print $2,$5}}' | awk '{{a[$1]=a[$1] FS $2} END{{for(i in a) print i a[i]}}' \
        | sed -e '1 i Founded Domains:' >> text/summary.txt |& tee -a {log}
        
        wget -O- https://rest.uniprot.org/uniprotkb/{UNIPROT_ID}.txt | grep  "^CC" \
        | sed 's/^\(CC\)//' | sed -e '1 i Info from Uniprot:' >> text/summary.txt |& tee -a {log}        
        """

rule msa:
    input:
        summary = "text/summary.txt"
    output:
        msa = "msa/msa.fasta"
    params:
        id = UNIPROT_ID
    log:
        "logs/msa.log"
    threads:
        workflow.cores
    message:
        "Creating MSA..."
    script:
        "scripts/msa.py"

rule find_sonservatives:
    input:
        msa = "msa/msa.fasta"
    output:
        data = "conservative/data.json",
        plot = "conservative/plot.png",
        pdb = "conservative/protein.pdb",
        pdb_render = "conservative/render.png"
    params:
        id = UNIPROT_ID
    log:
        "logs/conservatives.log"
    threads:
        workflow.cores
    message:
        "Finding conservative positions..."
    script:
        "scripts/conservative.py"

rule find_pockets:
    input:
        pdb = "conservative/protein.pdb",
    output:
        pockets = "fpocket/Pockets.zip",
        summary = "fpocket/Summary.json"
    log:
        "logs/find_pockets.log"
    threads:
        workflow.cores
    message:
        "Finding pockets..."
    script:
        "scripts/fpocket.py"

rule







