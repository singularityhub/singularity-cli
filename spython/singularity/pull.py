'''

Copyright (C) 2018 The Board of Trustees of the Leland Stanford Junior
University.
Copyright (C) 2018 Vanessa Sochat.

This program is free software: you can redistribute it and/or modify it
under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or (at your
option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT
ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Affero General Public
License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.

'''

from spython.logger import bot



    def pull(self,image_path,pull_folder='',
                             name_by_hash=False,
                             name_by_commit=False,
                             image_name=None,
                             size=None):

        '''pull will pull a singularity hub image
        :param image_path: full path to image / uris
        :param name_by: can be one of commit or hash, default is by image name
        ''' 

        if image_name is not None:
            name_by_hash=False
            name_by_commit=False

        final_image = None

        if not image_path.startswith('shub://') and not image_path.startswith('docker://'):
            bot.error("pull is only valid for docker and shub, %s is invalid." %image_name)
            sys.exit(1)           

        if self.debug is True:
            cmd = ['singularity','--debug','pull']
        else:
            cmd = ['singularity','pull']

        if pull_folder not in [None,'']:
            os.environ['SINGULARITY_PULLFOLDER'] = pull_folder
            pull_folder = "%s/" % pull_folder

        if image_path.startswith('shub://'):
            if image_name is not None:
                bot.debug("user specified naming pulled image %s" %image_name)
                cmd = cmd +["--name",image_name]
            elif name_by_commit is True:
                bot.debug("user specified naming by commit.")
                cmd.append("--commit")
            elif name_by_hash is True:
                bot.debug("user specified naming by hash.")
                cmd.append("--hash")
            # otherwise let the Singularity client determine own name
           
        elif image_path.startswith('docker://'):
            if size is not None:
                cmd = cmd + ["--size",size]
            if image_name is None:
                image_name = image_path.replace("docker://","").replace("/","-")
            final_image = "%s%s.simg" %(pull_folder,image_name)
            cmd = cmd + ["--name", final_image]
 
        cmd.append(image_path)
        bot.debug(' '.join(cmd))
        output = self.run_command(cmd)
        self.println(output)
        if final_image is None: # shub
            final_image = output.split('Container is at:')[-1].strip('\n').strip()
        return final_image

